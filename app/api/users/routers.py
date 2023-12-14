from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status, APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm
from app.api.common.env_manager import EnvManager
from .schemas import Token, UserSc, UserCreate, UserOut
from .managers import authenticate_user, get_current_active_user, create_user
from .utils import create_access_token 
from sqlalchemy.orm import Session
from app.db.postgres.connector import PostgreSqlManager

router = APIRouter()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(PostgreSqlManager.get_db)
):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=EnvManager.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserOut)
async def login_for_access_token(user_create: UserCreate, db: Session = Depends(PostgreSqlManager.get_db)):
    try:
        if user_create.password != user_create.verify_password:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Las contraseñas no coinciden")
        return await create_user(db, user_create)
    except HTTPException as http_exception:
        raise http_exception
