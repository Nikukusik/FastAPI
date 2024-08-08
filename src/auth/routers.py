import cloudinary
import cloudinary.uploader
from fastapi import APIRouter, Depends, HTTPException, Security, BackgroundTasks, UploadFile, File
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jinja2 import Environment, FileSystemLoader
from sqlalchemy.orm import Session
from starlette import status

from src.auth.email_utils import send_verification
from src.auth.models import Users_app
from src.auth.utils import verify_password, create_access_token, create_refresh_token, decode_access_token, create_verification_token, decode_verification_token

from config.general import CLOUDINARY_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from config.db import get_db
from src.auth.repo import UsersRepository
from src.auth.schema import UserResponse, Token, UserCreate

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="users_app/token")
env = Environment(loader=FileSystemLoader('src/templates'))

@router.post("/register")
def register(user_create: UserCreate, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    user = repo.get_user_by_email(user_create.email)
    if user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already exists")
    user = repo.create_user(user_create)
    verification_token = create_verification_token(user.email)
    verification_link = f"http://localhost:8000/users_app/verify_email?token={verification_token}"

    template = env.get_template('verification_email.html')
    body = template.render(verification_link=verification_link)

    background_tasks.add_task(send_verification, user.email, body)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content={"email": user.email})

@router.get("/verify_email")
def verify_email(token: str, db: Session = Depends(get_db)):
    email: str = decode_verification_token(token)
    repo = UsersRepository(db)
    user = repo.get_user_by_email(email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    repo.activate_user(user)
    return {"msg": "Email verified successfully"}



@router.post("/token", response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    user = repo.get_user_by_email(form_data.username)
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


@router.patch('/avatar', response_model=UserResponse)
async def update_avatar_user(file: UploadFile = File(), current_user: Users_app = Depends(get_current_user),
                             db: Session = Depends(get_db)):
    repo = UsersRepository(db)
    cloudinary.config(
        cloud_name=CLOUDINARY_NAME,
        api_key=CLOUDINARY_API_KEY,
        api_secret=CLOUDINARY_API_SECRET,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'NotesApp/{current_user.email}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'NotesApp/{current_user.email}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repo.update_avatar(current_user.email, src_url)
    return user
