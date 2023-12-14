from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class UserSc(BaseModel):
    username: str
    email: str = None
    is_active: bool = True


class UserInDB(UserSc):
    hashed_password: str

class UserCreate(UserSc):
    password: str
    verify_password: str

class UserOut(UserSc):
    pass