from sqlalchemy import Integer, String

from config.db import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Users_app(Base):
    __tablename__ = "users_app"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    users: Mapped[list["Users"]] = relationship("Users", back_populates="owner")
