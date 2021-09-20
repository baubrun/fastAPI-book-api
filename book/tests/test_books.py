from unittest import mock
import pytest
from fastapi.testclient import TestClient
from book.repositories.BookRepository import BookRepository, BookNotFoundError
from book.models import Book
from book.main import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_books(client):
    repository_mock = mock.Mock(spec=BookRepository)
    repository_mock.get_all.return_value = [
        Book(id=1, title='book1', year="2020", author_id=1),
    ]

    with app.container.book_repository.override(repository_mock):
        response = client.get('/books')

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {'id': 1, 'title': 'book1', 'year': "2020", 'author_id': 1},
    ]


def test_create_book(client):
    repository_mock = mock.Mock(spec=BookRepository)
    repository_mock.create(title='book1', year="2020", author_id=1)
    with app.container.book_repository.override(repository_mock):
        client.post('/books')
    repository_mock.create.assert_called_with(title='book1', year="2020", author_id=1)

def test_get_book_by_id(client):
    repository_mock = mock.Mock(spec=BookRepository)
    repository_mock.get_by_id.return_value = \
        Book(id=1, title='book1', year="2020", author_id=1)
    with app.container.book_repository.override(repository_mock):
        response = client.get('/books/1')
    assert response.status_code == 200
    data = response.json()
    assert data == {'id': 1, 'title': 'book1', 'year': "2020", 'author_id': 1}


def test_get_book_404(client):
    repository_mock = mock.Mock(spec=BookRepository)
    repository_mock.get_by_id.side_effect = BookNotFoundError(3)
    with app.container.book_repository.override(repository_mock):
        response = client.get('/books/3')
    assert response.status_code == 404