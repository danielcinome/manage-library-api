from pydantic import BaseModel
from typing import List, Optional

class BookBase(BaseModel):
    title: str
    subtitle: Optional[str]
    author: str
    category: str
    date_publication: str
    publisher: Optional[str]
    description: Optional[str]
    image_url: Optional[str]
    source_id: Optional[str]

class BookOut(BookBase):
    uuid: Optional[str] = None
    source: str

class BookCreate(BaseModel):
    source_id: str
    source: str
