from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.models import Book as BookDB
from .schemas import BookOut, BookCreate
from typing import List
from greenletio import async_
from app.api.integration.google_api import GoogleBooksIntegration
from app.api.integration.ny_times_api import NYTimesIntegration
from fastapi import HTTPException, status
import concurrent.futures

async def search_books(db: Session, query: str) -> List[BookOut]:
    try:
        if query:
            # Performs the search on all relevant attributes of the Book model.
            books = await async_(db.query(BookDB).filter(
                or_(
                    BookDB.title.ilike(f"%{query}%"),
                    BookDB.subtitle.ilike(f"%{query}%"),
                    BookDB.author.ilike(f"%{query}%"),
                    BookDB.category.ilike(f"%{query}%"),
                    BookDB.description.ilike(f"%{query}%"),
                )
            ).all)()
            if not books:
                # If no books are found in the internal database, search Google Books and New York time API.
                books_from_google = await GoogleBooksIntegration.search_books(query)
                books_from_ny_times = await NYTimesIntegration.search_books(query)

                google_books = books_from_google if books_from_google else []
                ny_times_books = books_from_ny_times if books_from_ny_times else []

                books = google_books + ny_times_books
                return books
        else:
            # If no 'query' is given, returns all books
            books = await async_(db.query(BookDB).all)()

        books = [BookOut(
            title=book.title,
            subtitle=book.subtitle,
            author=book.author,
            category=book.category,
            date_publication=book.date_publication.strftime("%Y-%m-%d %H:%M:%S"),
            publisher=book.publisher,
            description=book.description,
            image_url=book.image_url,
            source_id=book.source_id,
            uuid=str(book.uuid),
            source='db interna'
        ) for book in books]

        return books
    
    except HTTPException as http_exception:
        # Specifically handle HTTP exceptions
        raise http_exception
    except Exception as e:
        # Handle in a specific way according to the type of error that may occur
        raise HTTPException(status_code=500, detail=f"Error al buscar libros: {str(e)}")


async def create_book(db: Session, book_data: BookCreate) -> BookOut:
    try:
        # We check if the book already exists in the database.
        existing_book = db.query(BookDB).filter_by(source_id=book_data.source_id).first()
        if existing_book:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El libro ya existe en la base de datos")

        # We consult the corresponding source
        if book_data.source.lower() == 'google':
            book_info = await GoogleBooksIntegration.get_book_info(book_data.source_id)
        elif book_data.source.lower() == 'ny_times':
            book_info = await NYTimesIntegration.get_book_info(book_data.source_id)
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Fuente no válida")

        if not book_info:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado en la fuente especificada")

        # We create a new book in the database with the information obtained.
        new_book = BookDB(**book_info)
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        new_book.uuid = str(new_book.uuid)
        new_book.date_publication=new_book.date_publication.strftime("%Y-%m-%d %H:%M:%S")

        # We return the information of the book created
        return BookOut(
            **new_book.__dict__,
            source='db interna'
        )
    
    except HTTPException as http_exception:
        # Specifically handle HTTP exceptions
        raise http_exception
    except Exception as e:
        # Handle in a specific way according to the type of error that may occur
        raise HTTPException(status_code=500, detail=f"Error al crear el libro: {str(e)}")


async def delete_book(db: Session, uuid: str) -> BookOut:
    try:
        # We search for the book in the database by its uuid
        book_to_delete = await async_(db.query(BookDB).filter_by(uuid=uuid).first)()

        if not book_to_delete:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Libro no encontrado")

        # Delete the book from the database
        db.delete(book_to_delete)
        await async_(db.commit)()

        # We return the information of the deleted book
        return {
            'message': f'Se ha eliminado el registro del libro titulado, {book_to_delete.title}',
        }

    except HTTPException as http_exception:
        # Specifically handle HTTP exceptions
        raise http_exception
    except Exception as e:
        # Handle in a specific way according to the type of error that may occur
        raise HTTPException(status_code=500, detail=f"Error al eliminar el libro: {str(e)}")
