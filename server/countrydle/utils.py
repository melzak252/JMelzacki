import os
import json
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, DayCountry, Question, User
from qdrant.utils import get_fragments_matching_question
from qdrant import COLLECTION_NAME
from db.schemas.country import DayCountryDisplay
from db.repositories.countrydle import CountrydleRepository
from db.schemas.countrydle import GuessCreate, QuestionCreate


async def ask_question(
    question: str, day_country: DayCountry, user: User, session: AsyncSession
) -> Question:

    fragments = await get_fragments_matching_question(
        question, day_country, COLLECTION_NAME, session
    )
    context = "\n[ ... ]\n".join(fragment.text for fragment in fragments)
    country: Country = day_country.country

    system_prompt = f"""
    I want you to act as the game master for a country guessing game.
    Player tries to guess a specific country based on 'True' or 'False' answers to their questions.
    
    Answer questions True or False if you are fully confident of the answer.
    Answer question NA if you do not know answer for that question.
    Answer question Error if questions is not True/False question.
    
    Country to guess: {country.name}
    ### Country additional information:
    {context}
    ###
    
    ### Task
    You are answering the question with your best knowledge.
    Answer with JSON forma and nothing else. Use the specific format:
    {{
        "answer": "Choose only one of these options exactly: True | False | NA | Error",
        "explanation": "Your explanation for your answer"
    }}
    ### 
    
    ### Examples of answers
    Country: France. Question: Is your country known for its wines?
    {{
        "answer": "True",
        "explanation": "France is known for its Bordeaux, Champagne and many more!"
    }}
    
    Country: China. Question: Am I in Europe?
    {{
        "answer": "False",
        "explanation": "Chaina is located in Asia."
    }}
    
    Country: Czech Republic. Question: Are you in top 10 largest countries in the world?
    {{
        "answer": "False",
        "explanation": "Czech republic is not in top 10 largest countries."
    }}
    
    Country: Finland. Question: When your country declared independance?
    {{
        "answer": "Error",
        "explanation": "Question is not True\False question!"
    }}
    
    Country: France. Question: Is in your current president called Shrimp?
    {{
        "answer": "NA",
        "explanation": "I don't have current information to answer that question."
    }}
    
    Country: Chad. Question: ascap aso ndosiqn pa anjd
    {{
        "answer": "NA",
        "explanation": "Cannot understand the question!"
    }}
    """
    question_prompt = f"""Question: {question}"""

    prompts = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": question_prompt},
    ]
    model = os.getenv("QUIZ_MODEL")

    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=prompts,
        response_format={"type": "json_object"},
    )

    answer = response.choices[0].message.content

    try:
        answer_dict = json.loads(answer)
    except json.JSONDecodeError:
        print(answer)
        raise

    question_create = QuestionCreate(
        user_id=user.id,
        country_id=day_country.id,
        question=question,
        answer=answer_dict["answer"],
        explanation=answer_dict["explanation"],
        context=context,
    )
    return await CountrydleRepository(session).create_question(question_create)


async def give_guess(
    guess: str, daily_country: DayCountryDisplay, user: User, session: AsyncSession
):
    system_prompt = """
    I want you to act as the game master for a country guessing game.
    Player writes country and you have to say True if player guessed the country.
    
    Playher may use more casual name of country like USA, Holland, Pol etc.
    
    Answer guess True or False if you are fully confident of the answer.
    Answer guess NA if guess is confusing you.
    
    ### Task
    You are answering the question with your best knowledge.
    Answer with JSON forma and nothing else. Use the specific format:
    {{
        "answer": "Choose only one of these options exactly: True | False | NA",
    }}
    ### 
    
    ### Examples
    Country: Poland. Guess: Polska
    {
        "answer": "True"
    }
    
    Country: France. Guess: Franc
    {
        "answer": "True"
    }
    
    Country: China. Guess: China
    {
        "answer": "True"
    }
    
    Country: United States of America. Guess: USA 
    {
        "answer": "True"
    }
    
    Country: Germany. Guess: Austria
    {
        "answer": "False"
    }
    
    Country: Australia. Guess: Austria
    {
        "answer": "False"
    }
    
    Country: Kingdom of the Netherlands. Guess: Holland
    {
        "answer": "True"
    }
    
    Country: France. Guess: Germany or France
    {
        "answer": "NA"
    } # False because player tried to cheat. He can ask one guess at a time.
    """

    guess_prompt = f"Country: {daily_country.country_name}. Guess: {guess}"

    prompts = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": guess_prompt},
    ]
    model = os.getenv("QUIZ_MODEL")

    client = OpenAI()
    response = client.chat.completions.create(
        model=model,
        messages=prompts,
        response_format={"type": "json_object"},
    )

    answer = response.choices[0].message.content

    try:
        answer_dict = json.loads(answer)
    except json.JSONDecodeError:
        print(answer)
        raise

    guess_create = GuessCreate(
        guess=guess,
        day_id=daily_country.id,
        user_id=user.id,
        response=answer_dict["answer"],
    )
    return await CountrydleRepository(session).create_guess(guess_create)
