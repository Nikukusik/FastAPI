from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from repo import UsersRepository

from db import get_db
from schema import UsersResponse, UsersCreate, UsersUpdate

router = APIRouter()

@router.get("/", response_model=list[UsersResponse])
def get_users(limit: int=10, offset: int=0, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.get_contacts(limit, offset)

@router.post("/", response_model=UsersResponse)
def create_users(user: UsersCreate, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.create_contacts(user)

@router.get("/search/", response_model=list[UsersResponse])
def search(query: str, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.search(query)

@router.get("/birthdays", response_model=list[UsersResponse])
def get_upcoming_birthdays(db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.get_upcoming_birthdays()
@router.get("/{user_id}", response_model=UsersResponse)
def search_by_id(id: int, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.search_by_id(id)

@router.delete("/{user_id}")
def delete_by_id(id: int, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.delete_by_id(id)

@router.put("/{user_id}", response_model=UsersResponse)
def update_by_id(body: UsersUpdate, id: int, db:Session = Depends(get_db)):
    repo = UsersRepository(db)
    return repo.update_by_id(body, id)

