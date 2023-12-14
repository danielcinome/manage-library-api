# app/integration/open_library_api.py

import requests
from typing import List, Optional
from app.models.models import Book
from datetime import datetime
from app.api.books.schemas import BookOut, BookBase
from app.api.common.env_manager import EnvManager

class NYTimesIntegration:
    NY_TIMES_API_URL= EnvManager.NY_TIMES_API_URL
    NY_TIMES_API_KEY= EnvManager.NY_TIMES_API_KEY

    @classmethod
    async def search_books(cls, query: str) -> Optional[List[BookOut]]:
        params = {
            'title': query,
            'api-key': cls.NY_TIMES_API_KEY
        }
        response = requests.get(cls.NY_TIMES_API_URL, params=params)

        if response.status_code == 200:
            docs = response.json().get('results', [])
            books = [cls._convert_ny_times_doc_to_model(doc) for doc in docs]
            return books
        else:
            return None

    @classmethod
    async def get_book_info(cls, book_id: str):
        # Make the request to the NY Times Books API to get the book information by book ID.
        params = {
            'isbn': book_id,
            'api-key': cls.NY_TIMES_API_KEY
        }
        response = requests.get(cls.NY_TIMES_API_URL, params=params)
        
        if response.status_code == 200:
            response_json = response.json()
            book = response_json.get('results', {})
            book_data = cls._convert_ny_times_doc_to_model(book[0], True)
            del book_data['source']

            return book_data
        else:
            return None

    @staticmethod
    def _convert_ny_times_doc_to_model(book, to_created:bool=False) -> BookOut:
        source_id = book.get('isbns', '')[0].get('isbn13') if len(book.get('isbns', '')) > 0 else ''
        ranks_history = book.get('ranks_history', [])
        get_published_date = lambda source_id: next((item["published_date"] for item in ranks_history if item["primary_isbn13"] == source_id), None)
        published_date = get_published_date(source_id)

        # Map attributes from volume_info to the Book model
        book_data = {
            'title': book.get('title', ''),
            'subtitle': book.get('title_suggest', ''),
            'author': book.get('author', ''),
            'date_publication':  published_date,
            'category': '',
            'publisher': book.get('publisher', ''),
            'description': book.get('description', ''),
            'image_url': book.get('url', ''),
            'source': 'NY Times',
            'source_id':  source_id,
        }

        return BookOut(**book_data) if not to_created else book_data
