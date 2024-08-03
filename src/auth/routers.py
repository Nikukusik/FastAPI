from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from starlette import status

from src.auth.utils import verify_password, create_access_token, create_refresh_token, decode_access_token, \
    OAuth2PasswordRequestFormEmail

from config.db import get_db
from src.auth.repo import UsersRepository
from src.auth.schema import UserResponse, Token, UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/register")
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    user = repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"email": repo.create_user(user_create).email})


@router.post("/token", response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestFormEmail = Depends(), db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    user = repo.get_user_by_email(form_data.email)
    if not user or not verify_password(user.hashed_password, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    access_token = create_access_token(data={"sub": user.email})
    refresh_token = create_refresh_token(data={"sub": user.email})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_pype": "bearer",
    })

@router.post("/refresh", response_model=Token)
def refresh_token():
    pass


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UserResponse:
    credentials_exeption = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    token_data = decode_access_token(token)
    if token_data is None:
        raise credentials_exeption
    repo = UsersRepository(db)
    user = repo.get_user_by_email(token_data.email)
    if user is None:
        raise credentials_exeption
    return user

