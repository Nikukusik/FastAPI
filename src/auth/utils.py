from datetime import timedelta, timezone
from datetime import datetime as dtdt
from typing import Union

from fastapi import Form
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from os import getenv

from typing_extensions import Doc, Annotated

from src.auth.schema import TokenData

load_dotenv()

SECRET_KEY = getenv("SECRET_KEY")
ALGORITHM = getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
REFRESH_TOKEN_EXPIRE_DAYS = getenv("REFRESH_TOKEN_EXPIRE_DAYS")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(hashed_password: str, password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dtdt.now(timezone.utc) + expires_delta
    else:
        expire = dtdt.now(timezone.utc) + timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encoded_jwt

def create_refresh_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dtdt.now(timezone.utc) + expires_delta
    else:
        expire = dtdt.now(timezone.utc) + timedelta(days=int(REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
        return encoded_jwt

def decode_access_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            return None
        return TokenData(email=email)
    except JWTError:
        return None

class OAuth2PasswordRequestFormEmail(OAuth2PasswordRequestForm):
    def __init__(
            self,
            *,
            grant_type: Annotated[
                Union[str, None],
                Form(pattern="password"),
                Doc(
                    """
                    The OAuth2 spec says it is required and MUST be the fixed string
                    "password". Nevertheless, this dependency class is permissive and
                    allows not passing it. If you want to enforce it, use instead the
                    `OAuth2PasswordRequestFormStrict` dependency.
                    """
                ),
            ] = None,
            email: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `email` string. The OAuth2 spec requires the exact field name
                    `email`.
                    """
                ),
            ],
            password: Annotated[
                str,
                Form(),
                Doc(
                    """
                    `password` string. The OAuth2 spec requires the exact field name
                    `password".
                    """
                ),
            ],
            scope: Annotated[
                str,
                Form(),
                Doc(
                    """
                    A single string with actually several scopes separated by spaces. Each
                    scope is also a string.
    
                    For example, a single string with:
    
                    ```python
                    "items:read items:write users:read profile openid"
                    ````
    
                    would represent the scopes:
    
                    * `items:read`
                    * `items:write`
                    * `users:read`
                    * `profile`
                    * `openid`
                    """
                ),
            ] = "",
            client_id: Annotated[
                Union[str, None],
                Form(),
                Doc(
                    """
                    If there's a `client_id`, it can be sent as part of the form fields.
                    But the OAuth2 specification recommends sending the `client_id` and
                    `client_secret` (if any) using HTTP Basic auth.
                    """
                ),
            ] = None,
            client_secret: Annotated[
                Union[str, None],
                Form(),
                Doc(
                    """
                    If there's a `client_password` (and a `client_id`), they can be sent
                    as part of the form fields. But the OAuth2 specification recommends
                    sending the `client_id` and `client_secret` (if any) using HTTP Basic
                    auth.
                    """
                ),
            ] = None,
    ):
        self.grant_type = grant_type
        self.email = email
        self.password = password
        self.scopes = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret