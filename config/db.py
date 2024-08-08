from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.general import DATABASE_URL
from sqlalchemy.orm import declarative_base

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

