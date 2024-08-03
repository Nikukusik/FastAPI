from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.auth.models import Users_app

from src.auth.routers import get_current_user
from src.contacts.repo import UsersRepository

from config.db import get_db
from src.contacts.schema import UsersResponse, UsersCreate, UsersUpdate

router = APIRouter()

@router.get("/", response_model=list[UsersResponse])
def get_users(current_user: Users_app = Depends(get_current_user), limit: int=10, offset: int=0, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.get_contacts(limit, offset, current_user.id)

@router.post("/", response_model=UsersResponse)
def create_users(user: UsersCreate, current_user: Users_app = Depends(get_current_user), db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.create_contacts(user, current_user.id)

@router.get("/search/", response_model=list[UsersResponse])
def search(query: str, current_user: Users_app = Depends(get_current_user), db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.search(query, current_user.id)

@router.get("/birthdays", response_model=list[UsersResponse])
def get_upcoming_birthdays(current_user: Users_app = Depends(get_current_user), db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.get_upcoming_birthdays(current_user.id)
@router.get("/{user_id}", response_model=UsersResponse)
def search_by_id(id: int, current_user: Users_app = Depends(get_current_user), db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.search_by_id(id, current_user.id)

@router.delete("/{user_id}")
def delete_by_id(id: int, current_user: Users_app = Depends(get_current_user) , db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.delete_by_id(id, current_user.id)

@router.put("/{user_id}", response_model=UsersResponse)
def update_by_id(body: UsersUpdate, id: int, current_user: Users_app = Depends(get_current_user), db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.update_by_id(body, id, current_user.id)

