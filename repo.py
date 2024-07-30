from sqlalchemy import select, update

from models import User
from sqlalchemy.orm import Session

from schema import UsersCreate, UsersUpdate


class UsersRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_contacts(self, limit: int=10, offset: int=0):
        query = select(User).offset(offset).limit(limit)
        results = self.session.execute(query)
        return results.scalars().all()

    def create_contacts(self, user: UsersCreate):
        new_contact = User(**user.model_dump())
        self.session.add(new_contact)
        self.session.commit()
        self.session.refresh(new_contact)
        return new_contact.id
    def search(self, query: str):
        q = select(User).filter((User.first_name.contains(query))
                                  | (User.last_name.contains(query))
                                  | (User.email.contains(query)))

        res = self.session.execute(q)
        return res.scalars().all()

    def search_by_id(self, id):
        q = select(User).where(User.id == id)
        res = self.session.execute(q)
        return res.scalars().one()

    def delete_by_id(self, id):
        q = select(User).where(User.id == id)
        contact = self.session.execute(q).scalar_one()
        self.session.delete(contact)
        self.session.commit()

    def update_by_id(self, body: UsersUpdate, id):
        q = update(User).where(User.id == id).values(first_name=body.first_name,
                                                 last_name=body.last_name,
                                                 email=body.email,
                                                 phone=body.phone,
                                                 birthday=body.birthday)
        self.session.execute(q)
        self.session.commit()
        self.session.refresh()







