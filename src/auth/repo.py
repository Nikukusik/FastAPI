from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.models import Users_app
from src.auth.schema import UserCreate
from src.auth.utils import get_password_hash


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_create: UserCreate):
        hashed_password = get_password_hash(user_create.password)
        new_user = Users_app(email=user_create.email, hashed_password=hashed_password)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    def get_user_by_email(self, email):
        q = select(Users_app).where(Users_app.email == email)
        res = self.session.execute(q)
        return res.scalar_one_or_none()