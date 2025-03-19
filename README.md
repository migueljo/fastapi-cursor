# Dish Management API

A FastAPI application for managing restaurant dishes.

## Features

- Complete CRUD operations for dishes
- Input validation using Pydantic models
- Interactive API documentation with Swagger UI and ReDoc
- Proper error handling and status codes
- Pagination for listing dishes

## Installation

1. Clone the repository
2. Create a virtual environment and activate it:

```bash
# Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install the dependencies:

```bash
uv pip install fastapi uvicorn python-dotenv
```

## Configuration

The application can be configured using environment variables in a `.env` file:

## Running the Application

Start the application with:

```bash
# Using uvicorn directly
uvicorn main:app --reload

# Or using Python
python main.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- OpenAPI schema: http://localhost:8000/openapi.json

## Project Structure

```
dish-management-api/
├── main.py        # FastAPI application and routes
├── schemas.py     # Pydantic models for data validation
├── settings.py    # Application configuration
├── .env           # Environment variables
├── .gitignore     # Files to ignore in git
└── README.md      # Project documentation
```

## API Endpoints

The API provides the following endpoints:

- `GET /`: Welcome message
- `GET /health`: Health check
- `GET /dishes/`: List all dishes (with pagination)
- `GET /dishes/{dish_id}`: Get a specific dish
- `POST /dishes/`: Create a new dish
- `PUT /dishes/{dish_id}`: Update a dish completely
- `PATCH /dishes/{dish_id}`: Update a dish partially
- `DELETE /dishes/{dish_id}`: Delete a dish
