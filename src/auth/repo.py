from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.models import Users_app
from src.auth.schema import UserCreate
from src.auth.utils import get_password_hash


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_user(self, user_create: UserCreate):
        '''
        Creating User by schema user_create

        :param user_create: user_create
        :type user_create: object class user_create
        :return: The newly created user
        :rtype: class object Users_app
        '''
        hashed_password = get_password_hash(user_create.password)
        new_user = Users_app(email=user_create.email, hashed_password=hashed_password, verification=False)
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    def get_user_by_email(self, email: str):
        '''
        Getting user by email

        :param email: users email
        :type email: str
        :return: User by email
        :rtype: class object Users_app
        '''
        q = select(Users_app).where(Users_app.email == email)
        res = self.session.execute(q)
        return res.scalar_one_or_none()

    def activate_user(self, user: Users_app):
        '''
        Activating user by answer from his email

        :param user: Getting current user
        :type user: class object Users_app
        :return: Current User
        :rtype: class object Users_app
        '''
        user.verification = True
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def update_avatar(self, email: str, url: str):
        '''
        Updating users avatar

        :param email: Users email
        :type email: str
        :param url: url what's lead to page with new avatar
        :type: str
        :return: Current User
        :rtype: class object Users_app
        '''
        user = self.get_user_by_email(email)
        user.avatar = url
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user