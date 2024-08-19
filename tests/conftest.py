import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker


import config.general
from config.db import Base
from src.auth.models import Users_app
from src.auth.utils import get_password_hash

fake = Faker

engine = create_engine(config.general.DATABASE_TEST_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)



@pytest.fixture(scope="function", autouse=True)
def setup_db():
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)
        conn.run_sync(Base.metadata.create_all)
    yield
    with engine.begin() as conn:
        conn.run_sync(Base.metadata.drop_all)

@pytest.fixture(scope='function')
def db_session(setup_db):
    with SessionLocal() as session:
        yield session

@pytest.fixture(scope='function')
def test_password():
    return fake.password()

@pytest.fixture(scope='function')
def create_user(db: Session, test_password):
    hashed_password = get_password_hash(test_password)
    user_create = Users_app(email=fake.email, hashed_password=hashed_password)
    new_user = Users_app(email=user_create.email, hashed_password=user_create.hashed_password, verification=True)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user