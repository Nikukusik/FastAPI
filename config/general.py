from os import getenv

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = getenv("REFRESH_TOKEN_EXPIRE_DAYS")
VERIFICATION_TOKEN_EXPIRE_HOURS = getenv("VERIFICATION_TOKEN_EXPIRE_HOURS")
MAIL_USERNAME = getenv("MAIL_USERNAME", "test")
MAIL_PASSWORD = getenv("MAIL_PASSWORD", "test")
MAIL_FROM = getenv("MAIL_FROM", "admin@23web.com")
MAIL_PORT = getenv("MAIL_POST", 1025)
MAIL_SERVER = getenv("MAIL_SERVER", "localhost")
DATABASE_URL = getenv("DATABASE_URL")
REDIS_PORT = getenv("REDIS_PORT")
REDIS_HOST = getenv("REDIS_HOST")
CLOUDINARY_NAME = getenv("CLOUDINARY_NAME")
CLOUDINARY_API_KEY = getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = getenv("CLOUDINARY_API_SECRET")
DATABASE_TEST_URL = getenv("DATABASE_TEST_URL")
