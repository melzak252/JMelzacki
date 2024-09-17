import os
import json
from openai import OpenAI
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Country, DayCountry, Question, User
from qdrant.utils import get_fragments_matching_question, add_question_to_qdrant
from qdrant import COLLECTION_NAME
from schemas.country import DayCountryDisplay
from db.repositories.countrydle import CountrydleRepository
from schemas.countrydle import GuessCreate, QuestionCreate, QuestionEnhanced
from db.repositories.country import CountryRepository


async def enhance_question(question: str) -> QuestionEnhanced:
    system_prompt = """
You are an AI assistant for a game where players guess a country by asking True/False questions. 
Your task is to:

1. Receive a user's question.
2. Retrieve the meaning of the user's question.
3. Determine if it is a valid True/False question about possible country.
4. If It's valid then improve the question by make it more obvious about its intent.
5. If It's not valid then provide an explanation why the question is not valid.

### Output Format
Answer with JSON format and nothing else. 
Use the specific format:
{
  "valid": true | false,
  "question": "Improved question if question is valid",
  "explanation": "Explanation if question is not valid"
}

### Examples
User's Question: Is it in Europe?
Output: 
{
  "valid": true,
  "question": "Is the country located in Europe?"
}

User's Question: Tell me about its history
Output:
{
  "valid": false,
  "explanation": "This is not a True/False question."
}

User's Question: Is it seychelles?
{
  "valid": true,
  "question": "Is the country Seychelles?"
}

User's Question: Is this island/s country
{
  "valid": true,
  "question": "Is the country an island nation?"
}

User's Question: "asdfghjkl"
{
  "valid": false,
  "explanation": "The input is gibberish and not a valid True/False question."
}
"""

    question_prompt = f"""User's Question: {question}"""

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
        answer_dict: dict = json.loads(answer)
    except json.JSONDecodeError:
        print(answer)
        raise

    return QuestionEnhanced(
        original_question=question,
        valid=answer_dict["valid"],
        question=answer_dict.get("question", None),
        explanation=answer_dict.get("explanation", None),
    )


async def ask_question(
    question: QuestionEnhanced,
    day_country: DayCountry,
    user: User,
    session: AsyncSession,
) -> Question:

    fragments, question_vector = await get_fragments_matching_question(
        question.question, day_country, COLLECTION_NAME, session
    )
    context = "\n[ ... ]\n".join(fragment.text for fragment in fragments)
    country: Country = await CountryRepository(session).get(day_country.country_id)

    system_prompt = f"""
You are an AI assistant in a game where players try to guess a country by asking True/False questions. 
Your task is to:
1. Receive a valid True/False question from the player.
2. Use the provided country and context to answer the question accurately.

Instructions:
- Base your answers primarily on the provided context. If the context does not contain enough information, use your general knowledge to provide the most accurate answer possible.
- If you cannot determine the answer even with general knowledge, set "answer" to null.
- Incorporate any relevant details from the provided context about the country into your explanations.
- For any questions about events or information from April 2024 onwards, set "answer" to null

### Country to Guess: {country.name}
### Context: 
[...]
{context}
[...]

### Output Format
You are answering the question with your best knowledge.
Answer with JSON forma and nothing else. Use the specific format:
{{
"answer": true | false | null,
"explanation": "Your explanation for your answer."
}}
### 

### Examples of answers
Country: France. Question: Is your country known for its wines?
{{
    "answer": true,
    "explanation": "France is known for its Bordeaux, Champagne and many more!"
}}
Country: China. Question: Am I in Europe?
{{
    "answer": false,
    "explanation": "China is located in Asia."
}}
Country: Brazil. Question: Is the country's average annual rainfall over 2000 millimeters?
{{
    "answer": null,
    "explanation": "The question is too vague to answer correctly."
}}

Country: Japan. Question: Has the country hosted the 2025 World Expo?
{{
  "answer": null,
  "explanation": "I cannot provide information about events occurring after April 2024."
}}
"""
    question_prompt = f"""Question: {question.question}"""

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
        original_question=question.original_question,
        valid=question.valid,
        question=question.question,
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
