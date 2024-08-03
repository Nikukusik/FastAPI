from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, Date, ForeignKey
from config.db import Base

class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String, index=True)
    last_name: Mapped[str] = mapped_column(String, index=True)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    phone: Mapped[str] = mapped_column(String, index=True)
    birthday: Mapped[Date] = mapped_column(Date, index=True)
    owner_id: Mapped[int] = mapped_column(Integer, ForeignKey("users_app.id"), nullable=True)
    owner: Mapped["Users_app"] = relationship("Users_app", back_populates="users")



