from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import psycopg2
from dotenv import load_dotenv
from os import getenv
from sqlalchemy.orm import declarative_base

load_dotenv()

DATABASE_URL = getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def connect():
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(user="admin", password="admin") as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == "__main__":
    connect()

