from jose import jwt, JWTError
from fastapi import HTTPException
from pydantic import BaseModel
from sqlmodel import select, Session

from config import SECRET_KEY, ALGORITHM

from datetime import datetime, timedelta
from database import User
from typing import Optional

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    email: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(
    token: str, credentials_exception: HTTPException, session: Session
) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    statement = select(User).where(User.email == token_data.email)
    results = session.exec(statement)
    user = results.first()
    return user
