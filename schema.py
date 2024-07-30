from pydantic import BaseModel, EmailStr
from datetime import date
class UsersBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    birthday: date

class UsersResponse(UsersBase):
    id: int

class UsersCreate(UsersBase):
    pass

class UsersUpdate(UsersBase):
    pass