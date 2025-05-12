# Social Network API

A modular FastAPI application for a social network with users, posts, comments, likes, and favorites.

## Project Structure

The project follows a modular structure:

```
app/
├── core/              # Core configuration and database setup
│   ├── config.py      # Application configuration
│   └── database.py    # Database connection and session management
├── models/            # SQLAlchemy ORM models
│   ├── user.py        # User and Follow models
│   ├── post.py        # Post model
│   ├── comment.py     # Comment model
│   ├── like.py        # Like model
│   ├── favorite.py    # Favorite model
│   └── media.py       # Media model
├── schemas/           # Pydantic schemas for request/response validation
│   ├── user.py        # User schemas
│   ├── post.py        # Post schemas
│   ├── comment.py     # Comment schemas
│   ├── like.py        # Like schemas
│   ├── favorite.py    # Favorite schemas
│   ├── follow.py      # Follow schemas
│   └── media.py       # Media schemas
├── crud/              # CRUD operations for database interactions
│   ├── user.py        # User CRUD operations
│   ├── post.py        # Post CRUD operations
│   ├── comment.py     # Comment CRUD operations
│   ├── like.py        # Like CRUD operations
│   └── favorite.py    # Favorite CRUD operations
├── routers/           # API endpoints
│   ├── users.py       # User routes
│   ├── posts.py       # Post routes
│   ├── comments.py    # Comment routes
│   ├── likes.py       # Like routes
│   └── favorites.py   # Favorite routes
├── utils/             # Utility functions
│   └── auth.py        # Authentication utilities
└── main.py            # Application entry point
```

## Running the Application

### Using Docker Compose

```bash
docker-compose up -d
```

The API will be available at http://localhost:8000

### Without Docker

1. Set up a PostgreSQL database
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   uvicorn app.main:app --reload
   ```

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Authentication

This project includes a placeholder for JWT authentication in `app/utils/auth.py`. In a production environment, you would need to implement proper token-based authentication.
