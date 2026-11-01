from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models import Book, Loan
from app.schemas import LoanCreate

router = APIRouter(prefix="/loans", tags=["Loans"])


# Borrow a book
@router.post("", response_model=Loan, status_code=201)
def borrow_book(
    loan_data: LoanCreate,
    session: Session = Depends(get_session)
):
    book = session.get(Book, loan_data.book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies < 1:
        raise HTTPException(status_code=409, detail="Book is not available")

    loan = Loan(
        book_id=loan_data.book_id,
        borrower_name=loan_data.borrower_name
    )

    book.available_copies -= 1

    session.add(loan)
    session.add(book)
    session.commit()
    session.refresh(loan)

    return loan

# Get all loans
@router.get("", response_model=list[Loan])
def get_loans(
    active_only: bool = False,
    session: Session = Depends(get_session)
):
    statement = select(Loan)

    if active_only:
        statement = statement.where(Loan.is_returned == False)

    loans = session.exec(statement).all()

    return loans

# Return a borrowed book
@router.patch("/{loan_id}/return")
def return_book(
    loan_id: int,
    session: Session = Depends(get_session)
):
    loan = session.get(Loan, loan_id)

    if not loan:
        raise HTTPException(status_code=404, detail="Loan not found")

    if loan.is_returned:
        raise HTTPException(status_code=409, detail="Book already returned")

    book = session.get(Book, loan.book_id)

    loan.is_returned = True
    book.available_copies += 1

    session.add(loan)
    session.add(book)
    session.commit()

    return {"message": "Book returned successfully"}