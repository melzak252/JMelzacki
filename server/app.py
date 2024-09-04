from dotenv import load_dotenv
from fastapi_mail import MessageSchema
load_dotenv()

import datetime
from utils.app import lifespan
from countrydle import router as countrydle_router
from db import get_db
from db.repositories.user import UserRepository
from schemas.user import UserCreate, UserDisplay
from fastapi import BackgroundTasks, Depends, FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from users import router as users_router
from users.utils import create_access_token, create_verification_token, verify_email_token
from utils.email import fm, fm_noreply


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router, prefix="/users", tags=["users"])
app.include_router(countrydle_router, tags=["countrydle"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Game API!"}


@app.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db),
):
    user = await UserRepository(session).get_user(form_data.username)

    if not user or not UserRepository.verify_password(
        form_data.password, user.hashed_password
    ):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token = create_access_token(data={"sub": user.username})

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,  # Set to True in production
        samesite="Lax",
        path="/",
    )
    return {
        "access_token": access_token,
        "username": user.username,
        "token_type": "bearer",
    }


@app.post("/logout", status_code=status.HTTP_200_OK)
async def logout(response: Response):
    response.set_cookie(
        key="access_token",
        value="",
        httponly=True,
        secure=True,  # Set to True in production
        expires=datetime.datetime.now().isoformat(),
        samesite="Lax",
        path="/",
    )
    return {"success": 1}


@app.post("/register")
async def register(user: UserCreate, background_tasks: BackgroundTasks, session: AsyncSession = Depends(get_db)):
    new_user = await UserRepository(session).register_user(user=user)
    token = create_verification_token(new_user.email)
    
    verification_url = f"http://localhost:8080/verify-email?token={token}"
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[new_user.email],  # List of recipients
        subtype="html",
        template_body={"username": new_user.username, "verification_url": verification_url},
    )
    
    background_tasks.add_task(fm_noreply.send_message, message, template_name="verification_email.html")
    
    return {"message": "Verification email sent!"}


@app.get("/verify-email")
async def verify_email(token: str, session: AsyncSession = Depends(get_db)):
    email = verify_email_token(token)
    await UserRepository(session).verify_user_email(email)
    return {"message": "Email successfully verified"}
