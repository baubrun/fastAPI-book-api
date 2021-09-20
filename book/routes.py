from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status, Response
from .containers import Container
from .services import BookService, AuthorService
from . import schemas
from .repositories.BookRepository import BookNotFoundError
from .repositories.AuthorRepository import AuthorNotFoundError

router = APIRouter()


@router.get("/books")
@inject
def get_books(
        bookService: BookService = Depends(Provide[Container.book_service])):
    return bookService.get_all_books()


@router.get("/books/{book_id}")
@inject
def get_book(
        book_id: int,
        bookService: BookService = Depends(Provide[Container.book_service])):
    try:
        return bookService.get_book(book_id)
    except BookNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)



@router.post("/books", status_code=status.HTTP_201_CREATED)
@inject
def create_book(
        request: schemas.Book,
        bookService: BookService = Depends(Provide[Container.book_service])):
    return bookService.create_book(
        title=request.title,
        year=request.year,
        author_id=request.author_id
    )

@router.get("/authors")
@inject
def get_authors(
        authorService: AuthorService = Depends(Provide[Container.author_service])):
    return authorService.get_all_authors()


@router.get("/authors/{author_id}")
@inject
def get_author(author_id: int,
               authorService: AuthorService = Depends(Provide[Container.author_service])):
    try:
        return authorService.get_author(author_id)
    except AuthorNotFoundError:
        return Response(status_code=status.HTTP_404_NOT_FOUND)


@router.put("/authors/{author_id}")
@inject
def edit_author(request: schemas.Author, author_id: int,
                authorService: AuthorService = Depends(Provide[Container.author_service])):
    return authorService.edit_author(
        author_id=author_id,
        first_name=request.first_name,
        last_name=request.last_name)


@router.delete("/authors/{author_id}")
@inject
def delete_author(
        author_id: int,
        authorService: AuthorService = Depends(Provide[Container.author_service])):
    return authorService.delete_book(author_id)
