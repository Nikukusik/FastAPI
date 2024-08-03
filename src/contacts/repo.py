
from sqlalchemy import select

from src.contacts.models import Users
from sqlalchemy.orm import Session

from datetime import datetime as dtdt

from src.contacts.schema import UsersCreate, UsersUpdate


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_contacts(self, current_user_id: int, limit: int=10, offset: int=0):
        query = select(Users).where(Users.owner_id == current_user_id).offset(offset).limit(limit)
        results = self.session.execute(query)
        return results.scalars().all()

    def create_contacts(self, user: UsersCreate, current_user_id: int):
        new_contact = Users(**user.model_dump(), owner_id=current_user_id)
        self.session.add(new_contact)
        self.session.commit()
        self.session.refresh(new_contact)
        return new_contact
    def search(self, query: str, current_user_id: int):
        q = select(Users).where(Users.owner_id == current_user_id).filter((Users.first_name.contains(query))
                                  | (Users.last_name.contains(query))
                                  | (Users.email.contains(query)))

        res = self.session.execute(q)
        return res.scalars().all()

    def search_by_id(self, id, current_user_id: int):
        q = select(Users).where(Users.id == id, Users.owner_id == current_user_id)
        res = self.session.execute(q)
        return res.scalars().one()

    def delete_by_id(self, id, current_user_id: int):
        q = select(Users).where(Users.id == id, Users.owner_id == current_user_id)
        contact = self.session.execute(q).scalar_one()
        self.session.delete(contact)
        self.session.commit()

    def update_by_id(self, body: UsersUpdate, id, current_user_id: int):
        q = select(Users).filter_by(id=id, owner_id=current_user_id)
        res = self.session.execute(q)
        contact = res.scalar_one_or_none()
        if contact:
            contact.first_name = body.first_name
            contact.last_name = body.last_name
            contact.email = body.email
            contact.phone = body.phone
            contact.birthday = body.birthday
            self.session.commit()
            self.session.refresh(contact)
        return contact

    def get_upcoming_birthdays(self, current_user_id: int):
        query = select(Users).where(Users.owner_id == current_user_id)
        results = self.session.execute(query)
        users = results.scalars().all()
        tdate = dtdt.today().date()
        users_with_bth = []
        for user in users:
            bdate = user.birthday
            year_now = dtdt.today().year
            bdate = bdate.replace(year=year_now)
            days_between = (bdate - tdate).days
            if 0 <= days_between < 7:
                users_with_bth.append(user)
        if users_with_bth:
            return users_with_bth












