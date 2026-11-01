from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.database import get_session
from app.models import Book, Loan

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/summary")
def get_summary(session: Session = Depends(get_session)):

    books = session.exec(select(Book)).all()
    loans = session.exec(select(Loan)).all()

    total_books = len(books)

    total_copies = sum(book.total_copies for book in books)

    available_copies = sum(book.available_copies for book in books)

    active_loans = sum(1 for loan in loans if not loan.is_returned)

    return {
        "total_books": total_books,
        "total_copies": total_copies,
        "available_copies": available_copies,
        "active_loans": active_loans
    }