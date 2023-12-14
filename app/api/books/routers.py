from fastapi import APIRouter, Depends
from app.db.postgres.connector import PostgreSqlManager
from sqlalchemy.orm.session import Session
from typing import Annotated
from pydantic import BaseModel
from app.api.users.routers import get_current_active_user
from app.api.users.schemas import UserSc
from app.db.postgres.connector import PostgreSqlManager
from fastapi import Depends, HTTPException, status
from typing import List, Optional
from .managers import search_books, create_book, delete_book
from .schemas import BookOut, BookCreate


router = APIRouter()
validate_user = Annotated[UserSc, Depends(get_current_active_user)]

#
@router.get('/search')
async def get_books_by_query_router(query: Optional[str] = None, db: Session = Depends(PostgreSqlManager.get_db)):
    """
    Endpoint to search for books by any attribute.
    Example usage: /books?q=Elon musk
    """
    try:
        books = await search_books(db, query)
        if not books:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No se encontraron libros con el criterio de búsqueda.")
    except HTTPException as http_exception:
        raise http_exception

    return books


@router.post('/create')
async def create_book_router(
    book_data: BookCreate, current_user: validate_user, db: Session = Depends(PostgreSqlManager.get_db)
    ):
    """
    Endpoint to create a book in database according to its source and ID
    Example usage: source: google source_id: 123
    """
    try:
        return await create_book(db, book_data)
    except HTTPException as http_exception:
        raise http_exception

@router.delete("/delete/{uuid}")
async def delete_book_route(
    uuid: str, current_user: validate_user, db: Session = Depends(PostgreSqlManager.get_db)
    ):
    """
    Endpoint to delete the record of a book in the database according to its ID
    """
    try:
        return await delete_book(db, uuid)
    except HTTPException as http_exception:
        raise http_exception