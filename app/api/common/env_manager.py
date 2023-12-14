import os

from dotenv import load_dotenv

load_dotenv()

class EnvManager:
    SQLALCHEMY_DATABASE_URL: str = os.environ.get('SQLALCHEMY_DATABASE_URL')
    SECRET_KEY: str = os.environ.get('SECRET_KEY')
    ALGORITHM: str = os.environ.get('ALGORITHM', "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', 15))
    GOOGLE_BOOKS_API_URL: str = os.environ.get('GOOGLE_BOOKS_API_URL', "")
    NY_TIMES_API_URL: str = os.environ.get('NY_TIMES_API_URL', '')
    NY_TIMES_API_KEY: str = os.environ.get('NY_TIMES_API_KEY', '')
    TESTING_DB_URL:  str = os.environ.get('TESTING_DB_URL', 'sqlite:///./test_db.sqlite?check_same_thread=False')