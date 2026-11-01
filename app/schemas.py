from pydantic import BaseModel, Field
from typing import Optional


# New book add karne ke liye
class BookCreate(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    author: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=1)
    total_copies: int = Field(ge=1)


# Book update karne ke liye
class BookUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=3, max_length=120)
    author: Optional[str] = Field(default=None, min_length=2, max_length=80)
    category: Optional[str] = Field(default=None, min_length=1)


# Book borrow karne ke liye
class LoanCreate(BaseModel):
    book_id: int
    borrower_name: str = Field(min_length=2, max_length=80)