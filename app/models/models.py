from app.db.postgres.connector import PostgreSqlManager
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, UUID
import uuid
from datetime import datetime

class ChangesTracking(PostgreSqlManager.Base):

    __abstract__ = True

    created_on = Column(DateTime(), default=datetime.utcnow)
    updated_on = Column(DateTime(), default=datetime.utcnow,
                        onupdate=datetime.utcnow)

class User(ChangesTracking):
    __tablename__ = 'users'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                  unique=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    email = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)

class Book(ChangesTracking):
    __tablename__ = 'books'

    uuid = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                unique=True, nullable=False)
    title = Column(String, nullable=False)
    subtitle = Column(String)
    author = Column(String, nullable=False)
    category = Column(String)
    date_publication = Column(DateTime)
    publisher = Column(String)
    description = Column(String)
    image_url = Column(String)
    source_id = Column(String)
