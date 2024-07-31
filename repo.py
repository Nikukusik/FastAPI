
from sqlalchemy import select

from models import Users
from sqlalchemy.orm import Session

from schema import UsersCreate, UsersUpdate

import datetime as dt
from datetime import datetime as dtdt


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_contacts(self, limit: int=10, offset: int=0):
        query = select(Users).offset(offset).limit(limit)
        results = self.session.execute(query)
        return results.scalars().all()

    def create_contacts(self, user: UsersCreate):
        new_contact = Users(**user.model_dump())
        self.session.add(new_contact)
        self.session.commit()
        self.session.refresh(new_contact)
        return new_contact
    def search(self, query: str):
        q = select(Users).filter((Users.first_name.contains(query))
                                  | (Users.last_name.contains(query))
                                  | (Users.email.contains(query)))

        res = self.session.execute(q)
        return res.scalars().all()

    def search_by_id(self, id):
        q = select(Users).where(Users.id == id)
        res = self.session.execute(q)
        return res.scalars().one()

    def delete_by_id(self, id):
        q = select(Users).where(Users.id == id)
        contact = self.session.execute(q).scalar_one()
        self.session.delete(contact)
        self.session.commit()

    def update_by_id(self, body: UsersUpdate, id):
        q = select(Users).filter_by(id=id)
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

    def get_upcoming_birthdays(self):
        query = select(Users)
        results = self.session.execute(query)
        users = results.scalars().all()
        tdate = dtdt.today().date()
        birthdays = []
        for user in users:
            bdate = user["birthday"]
            bdate = dtdt.strptime(bdate, "%Y-%m-%d").date()
            year_now = dtdt.today().year
            bdate = bdate.replace(year=year_now)
            week_day = bdate.isoweekday()
            days_between = (bdate - tdate).days
            if 0 <= days_between < 7:
                if week_day < 6:
                    birthdays.append({"name": user["name"], 'congratulation_date': bdate.strftime("%Y-%m-%d")})
                else:
                    if (bdate + dt.timedelta(days=1)).weekday() == 0:
                        birthdays.append({'name': user['name'],
                                          'congratulation_date': (bdate + dt.timedelta(days=1)).strftime("%Y-%m-%d")})
                    elif (bdate + dt.timedelta(days=2)).weekday() == 0:
                        birthdays.append({'name': user['name'],
                                          'congratulation_date': (bdate + dt.timedelta(days=2)).strftime("%Y-%m-%d")})
        users = []
        if birthdays:
            for birthday in birthdays:
                users.append(self.search(birthday.get("name")))
            return users
        return results.scalars().first()











