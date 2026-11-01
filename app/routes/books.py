from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlmodel import Session, select

from app.database import get_session
from app.models import Book, Loan
from app.schemas import BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])


# 1. Add a new book
@router.post("", response_model=Book, status_code=201)
def create_book(book_data: BookCreate, session: Session = Depends(get_session)):

    book = Book(
        title=book_data.title,
        author=book_data.author,
        category=book_data.category,
        total_copies=book_data.total_copies,
        available_copies=book_data.total_copies
    )

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


# 2. Get all books

@router.get("", response_model=list[Book])
def get_books(
    search: str = None,
    category: str = None,
    available_only: bool = False,
    session: Session = Depends(get_session)
):
    statement = select(Book)

    if search:
        statement = statement.where(
            Book.title.ilike(f"%{search}%") |
            Book.author.ilike(f"%{search}%")
        )

    if category:
        statement = statement.where(
            Book.category == category
        )

    if available_only:
        statement = statement.where(
            Book.available_copies > 0
        )

    books = session.exec(statement).all()

    return books

# 3. Get one book
@router.get("/{book_id}", response_model=Book)
def get_book(book_id: int, session: Session = Depends(get_session)):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


# 4. Update a book
@router.patch("/{book_id}", response_model=Book)
def update_book(book_id: int, book_data: BookUpdate, session: Session = Depends(get_session)):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book, key, value)

    session.add(book)
    session.commit()
    session.refresh(book)

    return book


# 5. Delete a book
@router.delete("/{book_id}", status_code=204)
def delete_book(book_id: int, session: Session = Depends(get_session)):

    book = session.get(Book, book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    loan = session.exec(
        select(Loan).where(Loan.book_id == book_id)
    ).first()

    if loan:
        raise HTTPException(status_code=409, detail="Book has loan history")

    session.delete(book)
    session.commit()

    return Response(status_code=204)