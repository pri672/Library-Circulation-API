from typing import Optional
from sqlmodel import SQLModel, Field


class Book(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    title: str = Field(min_length=3, max_length=120)
    author: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=1)

    total_copies: int = Field(ge=1)
    available_copies: int = Field(ge=0)


class Loan(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )

    book_id: int = Field(foreign_key="book.id")
    borrower_name: str = Field(min_length=2, max_length=80)

    is_returned: bool = Field(default=False)