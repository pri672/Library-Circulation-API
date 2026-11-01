
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database import get_session


# Create a separate test database
test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)


@pytest.fixture
def client():
    SQLModel.metadata.create_all(test_engine)

    def get_test_session():
        with Session(test_engine) as session:
            yield session

    app.dependency_overrides[get_session] = get_test_session

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    SQLModel.metadata.drop_all(test_engine)


# Test 1: Create a book
def test_create_book(client):
    response = client.post(
        "/books",
        json={
            "title": "Python Basics",
            "author": "John Smith",
            "category": "Programming",
            "total_copies": 5
        }
    )

    assert response.status_code == 201
    assert response.json()["available_copies"] == 5


# Test 2: Get all books
def test_get_books(client):
    client.post(
        "/books",
        json={
            "title": "Database Systems",
            "author": "Robert Smith",
            "category": "Database",
            "total_copies": 3
        }
    )

    response = client.get("/books")

    assert response.status_code == 200
    assert len(response.json()) == 1


# Test 3: Borrow and return a book
def test_borrow_and_return_book(client):
    book_response = client.post(
        "/books",
        json={
            "title": "Web Development",
            "author": "David Miller",
            "category": "Technology",
            "total_copies": 2
        }
    )

    book_id = book_response.json()["id"]

    loan_response = client.post(
        "/loans",
        json={
            "book_id": book_id,
            "borrower_name": "Prity Das"
        }
    )

    assert loan_response.status_code == 201

    book = client.get(f"/books/{book_id}").json()
    assert book["available_copies"] == 1

    return_response = client.patch(
        f"/loans/{loan_response.json()['id']}/return"
    )

    assert return_response.status_code == 200

    book = client.get(f"/books/{book_id}").json()
    assert book["available_copies"] == 2


# Test 4: Book not found
def test_book_not_found(client):
    response = client.get("/books/999")

    assert response.status_code == 404
