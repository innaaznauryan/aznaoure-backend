import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests

from app.database import get_db
from app.repositories.user_repository import UserRepository
from app.schemas.user import UserSignup, UserLogin, GoogleAuthRequest, AuthResponse, UserOut
from app.utils.auth_utils import create_access_token

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
if not GOOGLE_CLIENT_ID:
    raise RuntimeError("GOOGLE_CLIENT_ID environment variable is not set")


@router.post("/signup", response_model=AuthResponse)
def signup(payload: UserSignup, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    existing = repo.get_by_email(payload.email)
    if existing:
        raise HTTPException(status_code=409, detail={"code": "email_already_exists"})

    hashed_password = pwd_context.hash(payload.password)
    user = repo.create(
        email=payload.email,
        hashed_password=hashed_password,
        first_name=payload.first_name,
        last_name=payload.last_name,
        phone=payload.phone,
    )

    access_token = create_access_token(data={"sub": str(user.id)})
    return AuthResponse(access_token=access_token, user=UserOut.model_validate(user))


@router.post("/login", response_model=AuthResponse)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_email(payload.email)

    if not user or not user.hashed_password or not pwd_context.verify(payload.password, user.hashed_password):
        raise HTTPException(status_code=401, detail={"code": "invalid_credentials"})

    access_token = create_access_token(data={"sub": str(user.id)})
    return AuthResponse(access_token=access_token, user=UserOut.model_validate(user))


@router.post("/google", response_model=AuthResponse)
def google_auth(payload: GoogleAuthRequest, db: Session = Depends(get_db)):
    try:
        id_info  = id_token.verify_oauth2_token(
            payload.credential, google_requests.Request(), GOOGLE_CLIENT_ID
        )
    except ValueError:
        raise HTTPException(status_code=401, detail={"code": "invalid_google_token"})

    google_id = id_info ["sub"]
    email = id_info ["email"]
    first_name = id_info .get("given_name", "")
    last_name = id_info .get("family_name", "")

    repo = UserRepository(db)
    user = repo.get_by_google_id(google_id)

    if not user:
        user = repo.get_by_email(email)

        if user:
            user = repo.link_google_id(user, google_id)
        else:
            user = repo.create(
                email=email,
                first_name=first_name,
                last_name=last_name,
                google_id=google_id,
            )

    access_token = create_access_token(data={"sub": str(user.id)})
    return AuthResponse(access_token=access_token, user=UserOut.model_validate(user))
