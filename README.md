Ran tool
Ran tool
Ran tool
Ran tool
Read file: app/main.py
Read file: pyproject.toml
Read file: app/routers/post.py
Read file: app/routers/users.py
Read file: app/routers/auth.py
Read file: app/schemas.py
Read file: app/models.py
Read file: app/database.py
Here is a comprehensive `README.md` for your project, based on the codebase:

---

# API-Postgres

A FastAPI-based RESTful API for managing users and posts, with JWT authentication and PostgreSQL as the backend database.

## Features

- User registration and authentication (JWT)
- CRUD operations for posts (each user can only access their own posts)
- Password hashing and secure login
- SQLAlchemy ORM with PostgreSQL
- Pydantic models for request/response validation

## Project Structure

```
.
├── app/
│   ├── main.py          # FastAPI app entry point
│   ├── models.py        # SQLAlchemy ORM models
│   ├── schemas.py       # Pydantic schemas
│   ├── database.py      # Database connection and session
│   ├── oauth2.py        # JWT token creation and verification
│   ├── utils.py         # Utility functions (e.g., password hashing)
│   └── routers/
│       ├── post.py      # Post-related API endpoints
│       ├── users.py     # User-related API endpoints
│       └── auth.py      # Authentication endpoints
├── pyproject.toml       # Project dependencies
├── uv.lock              # Lock file for dependencies
└── README.md            # Project documentation
```

## Setup

1. **Clone the repository:**

   ```bash
   git clone <your-repo-url>
   cd api-postgres
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

   Or, if using `uv`:

   ```bash
   uv pip install -r requirements.txt
   ```

3. **Configure the database:**

   - The default connection string is in `app/database.py`:
     ```
     postgresql+psycopg://postgres:password@host.docker.internal:5432/fastapi-postgres
     ```
   - Update as needed for your environment.

4. **Run the application:**
   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Authentication

- **POST `/login`**  
  Obtain a JWT access token.
  - Request: `username` (email), `password`
  - Response: `{ "access_token": "...", "token_type": "bearer" }`

### Users

- **POST `/users/`**  
  Register a new user.

  - Request: `{ "email": "...", "password": "..." }`
  - Response: User details (without password)

- **GET `/users/{id}`**  
  Get user details by ID.

### Posts (Authenticated)

All post endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

- **GET `/posts/`**  
  List all posts belonging to the authenticated user.

- **POST `/posts/`**  
  Create a new post.

  - Request: `{ "title": "...", "content": "...", "published": true }`

- **GET `/posts/{id}`**  
  Get a specific post by ID (only if owned by the user).

- **PUT `/posts/{id}`**  
  Update a post (only if owned by the user).

- **DELETE `/posts/{id}`**  
  Delete a post (only if owned by the user).

## Models

### User

- `id`: int
- `email`: str
- `password`: str (hashed)
- `created_at`: datetime

### Post

- `id`: int
- `title`: str
- `content`: str
- `published`: bool
- `created_at`: datetime
- `owner_id`: int (FK to User)

## Security

- Passwords are hashed using `passlib`.
- JWT tokens are used for authentication.
- Users can only access and modify their own posts.

## Dependencies

- FastAPI
- SQLAlchemy
- psycopg
- python-jose
- passlib
- uvicorn
