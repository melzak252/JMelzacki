import os
import json
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, DayCountry, Question, User
from qdrant.utils import get_fragments_matching_question, add_question_to_qdrant
from qdrant import COLLECTION_NAME
from schemas.country import DayCountryDisplay
from db.repositories.countrydle import CountrydleRepository
from schemas.countrydle import GuessCreate, QuestionCreate
from db.repositories.country import CountryRepository


async def ask_question(
    question: str, day_country: DayCountry, user: User, session: AsyncSession
) -> Question:

    fragments, question_vector = await get_fragments_matching_question(
        question, day_country, COLLECTION_NAME, session
    )
    context = "\n[ ... ]\n".join(fragment.text for fragment in fragments)
    country: Country = await CountryRepository(session).get(day_country.country_id)

    system_prompt = f"""
    You are the game master for a country guessing game where the player tries to guess a specific country based on your responses.

    ## Answer Guidelines:
        - True: If you are fully confident that the answer is accurate.
        - False: If you are fully confident that the answer is inaccurate.
        - NA: If you do not know the answer or if the information is not available.
        - Error: If the question is not a simple True/False question.
    
    ## Contextual Integration: 
        - Incorporate any relevant details from the provided context about the country into your explanations.

    ### Country to Guess: {country.name}
    ### context: 
    [...]
    {context}
    [...]

    ### Task
    You are answering the question with your best knowledge.
    Answer with JSON forma and nothing else. Use the specific format:
    {{
    "answer": "True | False | NA | Error",
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
    If a question is too ambiguous, respond with:
    {{
        "answer": "NA",
        "explanation": "The question is too vague to answer correctly."
    }}
    If the question contains unintelligible text (e.g., random characters), respond with:
    {{
        "answer": "Error",
        "explanation": "The question contains gibberish."
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
        day_id=day_country.id,
        question=question,
        answer=answer_dict["answer"],
        explanation=answer_dict["explanation"],
        context=context,
    )

    question_entity = await CountrydleRepository(session).create_question(
        question_create
    )
    await add_question_to_qdrant(question_entity, question_vector, country.id)
    return question_entity


async def give_guess(
    guess: str, daily_country: DayCountryDisplay, user: User, session: AsyncSession
):
    country: Country = await CountryRepository(session).get(daily_country.country_id)

    system_prompt = f"""
    You are the game master for a country guessing game. The player will guess a country, and you must determine if the guess is correct.

    Answering Guidelines:
        - True: If the player correctly guessed the country, including casual or abbreviated names (e.g., USA, Holland, Pol).
        - False: If the player's guess does not match the country.
        - NA: If the guess is unclear or confusing.
    
    Answer guess True or False if you are fully confident of the answer.
    Answer guess NA if guess is confusing you.

    Country to Guess: {country.name}

    ### Task: 
    Use your best knowledge to determine if the player's guess is correct. Respond only in JSON format as follows:
    {{
        "answer": "Choose only one of these options exactly: True | False | NA",
    }}
    ### 
    
    ### Examples
    Country: Poland. Guess: Polska
    {{
        "answer": "True"
    }}
    
    Country: France. Guess: Franc
    {{
        "answer": "True"
    }}
    
    Country: United States of America. Guess: USA 
    {{
        "answer": "True"
    }}
    
    Country: Germany. Guess: Austria
    {{
        "answer": "False"
    }}
    
    Country: Australia. Guess: Austria
    {{
        "answer": "False"
    }}
    
    Country: France. Guess: Germany or France
    {{
        "answer": "NA"
    }} # False because player tried to cheat. He can ask one guess at a time.
    """

    guess_prompt = f"Guess: {guess}"

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
