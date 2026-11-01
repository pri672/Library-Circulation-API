# Library Circulation API

A RESTful API for managing library books, borrowing records, and returning activities.

## 1. Project Overview

The Library Circulation API is a backend application designed to simplify library management. It helps maintain book records, manage borrowing and returning activities, and track book availability.

The application provides different API endpoints to create, retrieve, update, search, filter, and delete books. It also manages loan records and generates summary reports.

## 2. Technologies Used

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Pydantic

## 3. Key Features

- Add new books to the library.
- View all books and individual book details.
- Update book information.
- Delete books that have no loan history.
- Borrow available books.
- Return borrowed books.
- Search books by title or author.
- Filter books by category.
- View only available books.
- Track active and returned loans.
- Generate library summary reports.
- Validate input data and handle errors.

## 4. Project Structure

```text
LibraryAPI/
│
├── app/
│   ├── routes/
│   │   ├── books.py
│   │   ├── loans.py
│   │   └── reports.py
│   │
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
├── requirements.txt
├── README.md
└── .gitignore
```

## 5. Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/pri672/Library-Circulation-API.git
cd LibraryAPI
```

### Step 2: Create a Virtual Environment

```bash
python3 -m venv .venv
```

### Step 3: Activate the Virtual Environment

```bash
source .venv/bin/activate
```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Run the Application

```bash
uvicorn app.main:app --reload
```

## 6. API Documentation

After starting the server, open:

http://127.0.0.1:8000/docs

The interactive Swagger documentation allows users to test all available API endpoints.

## 7. API Endpoints

### Books

| Method | Endpoint | Description |
|---|---|---|
| POST | /books | Create a new book |
| GET | /books | Get all books |
| GET | /books/{book_id} | Get a single book |
| PATCH | /books/{book_id} | Update book details |
| DELETE | /books/{book_id} | Delete a book |

### Loans

| Method | Endpoint | Description |
|---|---|---|
| POST | /loans | Borrow a book |
| GET | /loans | Get all loans |
| PATCH | /loans/{loan_id}/return | Return a borrowed book |

### Reports

| Method | Endpoint | Description |
|---|---|---|
| GET | /reports/summary | Get library summary |

## 8. Database Management

The application uses SQLite as its database.

SQLModel manages database models and relationships. Book and Loan records are stored in the database.

The database tables are created automatically when the application starts.

## 9. Error Handling

The API uses appropriate HTTP status codes:

- **200** – Successful request
- **201** – Resource created successfully
- **204** – Resource deleted successfully
- **404** – Resource not found
- **409** – Conflict, such as unavailable books or existing loan history
- **422** – Input validation error

## 10. Testing

The API can be tested using the interactive Swagger UI at:

http://127.0.0.1:8000/docs

The tests cover book management, borrowing, returning, filtering, and report functionality.

## 11. Conclusion

The Library Circulation API provides an organized way to manage library books and borrowing activities. It helps maintain accurate book availability, track loan records, and retrieve useful library information through RESTful API endpoints.

## Author

Developed as a Python backend project.