from sqlalchemy.orm import Session
from contextlib import AbstractContextManager
from typing import Callable, Iterator
from ..models import Author


class NotFoundError(Exception):
    entity_name: str

    def __init__(self, entity_id):
        super().__init__(f'{self.entity_name} not found, id: {entity_id}')


class AuthorNotFoundError(NotFoundError):
    entity_name: str = 'Author'


class AuthorRepository:
    def __init__(self,
                 session_factory: Callable[..., AbstractContextManager[Session]]) -> None:
        self.session_factory = session_factory

    def get_all(self) -> Iterator[Author]:
        with self.session_factory() as session:
            return session.query(Author).all()

    def get_by_id(self, author_id) -> Author:
        with self.session_factory() as session:
            author = session.query(Author).filter(Author.id == author_id).first()
        if not author:
            raise AuthorNotFoundError(author_id)
        return author

    def create_author(self, first_name: str, last_name: str, created: str) -> Author:
        with self.session_factory() as session:
            new_author = Author(
                first_name=first_name,
                last_name=last_name,
                created=created
            )
            session.add(new_author)
            session.commit()
            session.refresh(new_author)
            return new_author

    def edit_author(self, author_id: int, first_name: str, last_name: str, created: str) -> Author:
        with self.session_factory() as session:
            new_author = Author(
                author_id=author_id,
                first_name=first_name,
                last_name=last_name,
                created=created
            )
            session.add(new_author)
            session.commit()
            session.refresh(new_author)
            return new_author

    def delete_by_id(self, author_id: int) -> None:
        with self.session_factory() as session:
            author: Author = session.query(Author).filter(Author.id == author_id).first()
            if not author:
                raise AuthorNotFoundError(author_id)
            session.delete(author)
            session.commit()
