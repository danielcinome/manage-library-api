from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from app.db import Base
from app.api.common.env_manager import EnvManager


engine = create_engine(
    EnvManager.SQLALCHEMY_DATABASE_URL
)

class PostgreSqlManager:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = Base

    @classmethod
    def get_db(cls):
        db = cls.SessionLocal()
        try:
            yield db
        finally:
            db.close()