from ..repositories import BookRepository
from ..models import Book
from typing import Iterator


class BookService:
    def __init__(self, book_repository: BookRepository):
        self._repository = book_repository

    def get_all_books(self) -> Iterator[Book]:
        return self._repository.get_all()

    def get_book(self, book_id: int) -> Book:
        return self._repository.get_by_id(book_id)

    def create_book(self, title: str, year: str, author_id: int) -> Book:
        return self._repository.create(
            title=title,
            year=year,
            author_id=author_id
        )

    def delete_book(self, book_id: int) -> None:
        return self._repository.delete_by_id(book_id)
