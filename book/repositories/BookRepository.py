from typing import Callable, Iterator
from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from ..models import Book
from ..schemas import Book as BookSchema

class BookRepository:

    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Book]:
        with self.session_factory() as session:
            return session.query(Book).all()

    def get_by_id(self, book_id) -> Book:
        with self.session_factory() as session:
            book = session.query(Book).filter(Book.id == book_id).first()
        if not book:
            raise BookNotFoundError(book_id)
        return book

    def create(self, title: str, year: str, author_id: str) -> BookSchema:
        with self.session_factory() as session:
            new_book = Book(
                title=title,
                year=year,
                author_id=author_id
            )
            session.add(new_book)
            session.commit()
            session.refresh(new_book)
            return new_book

    def delete_by_id(self, book_id: int) -> None:
        with self.session_factory() as session:
            book: Book = session.query(Book).filter(Book.id == book_id).first()
            if not book:
                raise BookNotFoundError(book_id)
            session.delete(book)
            session.commit()


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class BookNotFoundError(NotFoundError):
    entity_name: str = 'Book'
