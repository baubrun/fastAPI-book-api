from dependency_injector import containers, providers

from .db import Database
from .repositories.BookRepository import BookRepository
from .repositories.AuthorRepository import AuthorRepository
from .services.BookService import BookService
from .services.AuthorService import AuthorService
from dotenv import load_dotenv
import os
load_dotenv()
class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    db = providers.Singleton(Database, db_url=os.getenv("DB_URL"))

    book_repository = providers.Factory(
        BookRepository,
        session_factory=db.provided.session
    )

    book_service = providers.Factory(
        BookService,
        book_repository=book_repository,
    )

    author_repository = providers.Factory(
        AuthorRepository,
        session_factory=db.provided.session
    )

    author_service = providers.Factory(
        AuthorService,
        author_repository=author_repository,
    )