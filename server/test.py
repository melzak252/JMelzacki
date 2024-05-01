from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
import openai
from random import choice
from fastapi.middleware.cors import CORSMiddleware
import os
from pycountry import countries

# Load environment variables
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=api_key)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify domains for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

current_country = None

def get_country_state():
    global current_country
    if current_country is None:
        current_country = choice(list(countries))
        
    state = {"country": current_country}
    return state
  
class Guess(BaseModel):
    guess: str

class Query(BaseModel):
    question: str

@app.post("/ask/")
async def ask_question(query: Query, state: dict = Depends(get_country_state)):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Adjust the model as necessary
        messages=[
            {"role": "system", "content": """
You are the game master for a guessing game where the player tries to guess a specific country based on 'True' or 'False' answers to their questions.
Players may ask about the identity of the country in various forms, such as 'Are you XXX?', 'Am I XXX?', 'Am I in XXX?', 'Is my country XXX?', or 'Is your country XXX?'. 
Regardless of how the question is phrased, you should only answer with 'True' or 'False'.
Do not provide any hints or additional information. 
Players can call themselves a country 
"""},
            {"role": "user", "content": f"Country: {state['country'].name}. Question: {query.question}"}
        ],
        temperature=0
    )
    return {"answer": response.choices[0].message.content}


@app.get("/restart/")
async def start_game(state: dict = Depends(get_country_state)):
    # Set up a new game session
    global current_country
    current_country = None
    return {"message": "Game started! Guess the country."}

@app.get("/get_current/")
async def start_game(state: dict = Depends(get_country_state)):
    # Set up a new game session
    global current_country
    return {"country": current_country}
