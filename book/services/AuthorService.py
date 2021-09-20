from ..repositories.AuthorRepository import AuthorRepository
from ..models import Author
from typing import Iterator


class AuthorService:
    def __init__(self, author_repository: AuthorRepository):
        self._repository = author_repository

    def get_all_authors(self) -> Iterator[Author]:
        return self._repository.get_all()

    def edit_author(self, author_id: int, first_name: str, last_name: str, created: str):
            return self._repository.edit_author(
                author_id=author_id,
                first_name=first_name,
                last_name=last_name,
                created=created)

    def get_author(self, author_id: int) -> Author:
        return self._repository.get_by_id(author_id)

    def create_author(self, first_name: str, last_name: str, created: str) -> Author:
        return self._repository.create_author(
            first_name=first_name,
            last_name=last_name,
            created=created)

    def delete_author(self, author_id: int) -> None:
        return self._repository.delete_by_id(author_id)
