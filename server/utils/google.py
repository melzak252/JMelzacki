


from dotenv import load_dotenv
from fastapi import HTTPException
from jose import JWTError
load_dotenv()
import os
import requests


GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_OAUTH2_URL = "https://oauth2.googleapis.com/tokeninfo?id_token="

def verify_google_token(token: str):
    try:
        # Call Google's OAuth2 tokeninfo endpoint to verify the token
        response = requests.get(f"{GOOGLE_OAUTH2_URL}{token}")
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Invalid Google Token")
        
        token_info = response.json()

        # Check if the token was issued to your app's client
        if token_info["aud"] != GOOGLE_CLIENT_ID:
            raise HTTPException(status_code=400, detail="Token not issued for this app!")
        
        
        if not token_info["email_verified"]:
            raise HTTPException(status_code=400, detail="Email is not verified!")

        return token_info

    except JWTError as e:
        raise HTTPException(status_code=400, detail="Token verification failed")