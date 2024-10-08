from typing import Union
from db import get_db
from db.models import User
from db.repositories.countrydle import CountrydleRepository
from schemas.countrydle import (
    CountrydleEndState,
    CountrydleState,
    FullUserHistory,
    GuessBase,
    GuessDisplay,
    InvalidQuestionDisplay,
    QuestionBase,
    QuestionCreate,
    QuestionDisplay,
    UserHistory,
)
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from countrydle import history
from users.utils import get_current_user

import countrydle.utils as gutils

load_dotenv()

router = APIRouter(prefix="/countrydle")

router.include_router(history.router)


@router.get("/state", response_model=CountrydleState)
async def get_state(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    daily_country = await CountrydleRepository(session).get_today_country()

    game_state = await CountrydleRepository(session).get_game_state(user, daily_country)
    return game_state


@router.get("/end", response_model=CountrydleEndState)
async def get_end_state(
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    daily_country = await CountrydleRepository(session).get_today_country()

    if not await CountrydleRepository(session).is_player_game_over(user, daily_country):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The player is still playing the game!",
        )

    end_state = await CountrydleRepository(session).get_end_game_state(
        user, daily_country
    )

    return end_state


@router.post("/guess", response_model=GuessDisplay)
async def get_game(
    guess: GuessBase,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    daily_country = await CountrydleRepository(session).get_today_country()

    if (
        len(
            await CountrydleRepository(session).get_guesses_for_user_day(
                user, daily_country
            )
        )
        >= 3
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User cannot guess more times than 3!",
        )

    return await gutils.give_guess(
        guess=guess.guess, daily_country=daily_country, user=user, session=session
    )


@router.post("/question", response_model=Union[QuestionDisplay, InvalidQuestionDisplay])
async def ask_question(
    question: QuestionBase,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    day_country = await CountrydleRepository(session).get_today_country()

    if await CountrydleRepository(session).is_player_game_over(user, day_country):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User finished the game already!",
        )

    if (
        len(
            await CountrydleRepository(session).get_questions_for_user_day(
                user, day_country
            )
        )
        >= 10
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User cannot ask more questions than 10!",
        )

    enh_question = await gutils.enhance_question(question.question)
    if not enh_question.valid:
        question_create = QuestionCreate(
            user_id=user.id,
            day_id=day_country.id,
            original_question=enh_question.original_question,
            valid=enh_question.valid,
            question=enh_question.question,
            answer=None,
            explanation=enh_question.explanation,
            context=None,
        )
        new_quest = await CountrydleRepository(session).create_question(question_create)

        return InvalidQuestionDisplay.model_validate(new_quest)

    new_quest = await gutils.ask_question(
        question=enh_question,
        day_country=day_country,
        user=user,
        session=session,
    )
    return QuestionDisplay.model_validate(new_quest)


@router.get("/result", response_model=FullUserHistory)
async def player_result(
    user: User = Depends(get_current_user), session: AsyncSession = Depends(get_db)
):
    daily_country = await CountrydleRepository(session).get_today_country()

    if not CountrydleRepository(session).is_player_game_over(user, daily_country):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Player is still playing the game!",
        )

    return await CountrydleRepository(session).get_player_full_histiory_for_today(
        user, daily_country
    )
