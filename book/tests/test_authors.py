from unittest import mock
import pytest
from fastapi.testclient import TestClient
from book.repositories.AuthorRepository import AuthorRepository, AuthorNotFoundError
from book.models import Author
from book.main import app


@pytest.fixture
def client():
    yield TestClient(app)


def test_get_authors(client):
    repository_mock = mock.Mock(spec=AuthorRepository)
    repository_mock.get_all.return_value = [
        Author(
            id=1,
            first_name="john",
            last_name="doe",
            created="today")
    ]

    with app.container.author_repository.override(repository_mock):
        response = client.get("/authors")

    assert response.status_code == 200
    data = response.json()
    assert data == [
        {"id": 1,"first_name": "john", "last_name": "doe", "created": "today"}
    ]


def test_create_author(client):
    repository_mock = mock.Mock(spec=AuthorRepository)
    repository_mock.create_author(first_name="john",
                           last_name="doe",
                           created="today")
    with app.container.author_repository.override(repository_mock):
        client.post("/authors")
    repository_mock.create_author.assert_called_with(first_name="john",
                                              last_name="doe",
                                              created="today")


def test_get_author_by_id(client):
    repository_mock = mock.Mock(spec=AuthorRepository)
    repository_mock.get_by_id.return_value = \
        Author(id=1, first_name="john", last_name="doe", created="today")
    with app.container.author_repository.override(repository_mock):
        response = client.get("/authors/1")
    assert response.status_code == 200
    data = response.json()
    assert data == {"id": 1, "first_name": "john", "last_name": "doe", "created": "today"}


def test_get_author_404(client):
    repository_mock = mock.Mock(spec=AuthorRepository)
    repository_mock.get_by_id.side_effect = AuthorNotFoundError(3)
    with app.container.author_repository.override(repository_mock):
        response = client.get("/authors/3")

    assert response.status_code == 404
