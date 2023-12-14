from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from app.api.common.env_manager import EnvManager
from .schemas import TokenData, UserSc, UserInDB, UserCreate
from .utils import verify_password, get_password_hash
from sqlalchemy.orm import Session
from app.models.models import User
from app.db.postgres.connector import PostgreSqlManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_user(db: Session, username: str):
    user = db.query(User).filter_by(username=username).first()
    if user:
        return UserInDB(
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            hashed_password=user.hashed_password,
        )
    return None

def authenticate_user(db: Session, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(PostgreSqlManager.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, EnvManager.SECRET_KEY, algorithms=[EnvManager.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)]
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def create_user(db: Session, user_data: UserCreate) -> UserSc:
    hashed_password = get_password_hash(user_data.password)
    new_user = User(username=user_data.username, hashed_password=hashed_password, email=user_data.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user