from fastapi import FastAPI

from app.database import create_db_and_tables
from app import models
from app.routes import books, loans, reports

app = FastAPI(title="Library Circulation API")


@app.on_event("startup")
def startup():
    create_db_and_tables()


app.include_router(books.router)
app.include_router(loans.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {"message": "Library API is running"}