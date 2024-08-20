import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from faker import Faker


from config.general import DATABASE_TEST_URL
from config.db import Base, get_db
from main import app
from src.auth.models import Users_app
from src.auth.utils import get_password_hash, create_access_token, create_refresh_token

fake = Faker()

engine = create_engine(DATABASE_TEST_URL, echo=True)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)



@pytest.fixture(scope="function", autouse=True)
def setup_db():
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)
        Base.metadata.create_all(bind=conn)
    yield
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)

@pytest.fixture(scope='function')
def db_session(setup_db):
    with SessionLocal() as session:
        yield session

@pytest.fixture(scope='function')
def user_password():
    return fake.password()

@pytest.fixture(scope='function')
def create_user(db_session: Session, user_password):
    hashed_password = get_password_hash(user_password)
    new_user = Users_app(
        email=fake.email(),
        hashed_password=hashed_password,
        verification=True)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user)
    return new_user

@pytest.fixture(scope='function')
def override_get_db(db_session):
    def _get_db():
        with db_session as session:
            yield session
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture(scope='function')
def auth_headers(create_user):
    access_token = create_access_token(data={"sub": create_user.email})
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    return headers

@pytest.fixture(scope="function")
def token(create_user):
    return create_access_token(data={"sub": create_user.email})
