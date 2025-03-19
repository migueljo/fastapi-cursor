from fastapi import FastAPI, HTTPException, status, Response, Path, Query
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware

from settings import settings
from schemas import Dish

# Create the FastAPI application
app = FastAPI(
    title=settings.APP_TITLE,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

"""
FastAPI application for dish management.
This API provides a complete CRUD interface for managing dishes in a restaurant.
"""

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Example list to store dishes (simulating a database)
dishes_db = []

# Root route
@app.get("/", tags=["Root"])
def read_root():
    """
    Root endpoint that returns a welcome message.
    
    Returns:
        dict: A welcome message for the API
    """
    return {"message": "Welcome to the FastAPI Dish Management API"}

# Check application status
@app.get("/health", tags=["Health"])
def check_health():
    """
    Health check endpoint to monitor API status.
    
    Returns:
        dict: Status information about the API
    """
    return {"status": "ok"}

# CREATE - Create a new dish
@app.post("/dishes/", response_model=Dish, status_code=status.HTTP_201_CREATED, tags=["Dishes"])
def create_dish(dish: Dish):
    """
    Create a new dish in the database.
    
    Args:
        dish (Dish): The dish object to create
    
    Returns:
        Dish: The created dish with its assigned ID
    
    Raises:
        HTTPException: If a dish with the provided ID already exists
    """
    dish_dict = dish.model_dump()
    
    # If no ID is provided, we generate one automatically
    if dish.id is None:
        dish_dict["id"] = len(dishes_db) + 1
    elif any(d["id"] == dish.id for d in dishes_db):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Dish with id {dish.id} already exists"
        )
    
    dishes_db.append(dish_dict)
    return dish_dict

# READ - Get all dishes
@app.get("/dishes/", response_model=List[Dish], tags=["Dishes"])
def read_dishes(
    skip: int = Query(0, description="Number of dishes to skip", ge=0),
    limit: int = Query(100, description="Maximum number of dishes to return", ge=1, le=100)
):
    """
    Get a list of all available dishes with pagination.
    
    Args:
        skip (int, optional): Number of dishes to skip. Defaults to 0.
        limit (int, optional): Maximum number of dishes to return. Defaults to 100.
    
    Returns:
        List[Dish]: A list of dish objects
    """
    return dishes_db[skip: skip + limit]

# READ - Get a specific dish by ID
@app.get("/dishes/{dish_id}", response_model=Dish, tags=["Dishes"])
def read_dish(
    dish_id: int = Path(..., description="ID of the dish to retrieve", ge=1)
):
    """
    Get a specific dish by its ID.
    
    Args:
        dish_id (int): ID of the dish to retrieve
    
    Returns:
        Dish: The requested dish object
    
    Raises:
        HTTPException: If the dish with the specified ID is not found
    """
    for dish in dishes_db:
        if dish["id"] == dish_id:
            return dish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with id {dish_id} not found"
    )

# UPDATE - Update an existing dish
@app.put("/dishes/{dish_id}", response_model=Dish, tags=["Dishes"])
def update_dish(
    dish_id: int = Path(..., description="ID of the dish to update", ge=1),
    dish: Dish = None
):
    """
    Update an existing dish completely.
    
    Args:
        dish_id (int): ID of the dish to update
        dish (Dish): New dish data to replace the existing dish
    
    Returns:
        Dish: The updated dish object
    
    Raises:
        HTTPException: If the dish with the specified ID is not found
    """
    for idx, stored_dish in enumerate(dishes_db):
        if stored_dish["id"] == dish_id:
            # Make sure the ID in the path and in the body match
            dish_dict = dish.model_dump()
            dish_dict["id"] = dish_id
            dishes_db[idx] = dish_dict
            return dish_dict
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with id {dish_id} not found"
    )

# UPDATE - Partially update a dish (PATCH)
@app.patch("/dishes/{dish_id}", response_model=Dish, tags=["Dishes"])
def partial_update_dish(
    dish_id: int = Path(..., description="ID of the dish to partially update", ge=1),
    name: Optional[str] = None,
    price: Optional[float] = Query(None, gt=0, description="Price of the dish (must be greater than 0)")
):
    """
    Partially update an existing dish.
    
    Args:
        dish_id (int): ID of the dish to update
        name (str, optional): New dish name. Defaults to None.
        price (float, optional): New dish price (must be greater than 0). Defaults to None.
    
    Returns:
        Dish: The updated dish object
    
    Raises:
        HTTPException: If the dish with the specified ID is not found
    """
    for idx, stored_dish in enumerate(dishes_db):
        if stored_dish["id"] == dish_id:
            if name is not None:
                dishes_db[idx]["name"] = name
            if price is not None:
                dishes_db[idx]["price"] = price
            return dishes_db[idx]
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with id {dish_id} not found"
    )

# DELETE - Delete a dish
@app.delete("/dishes/{dish_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Dishes"])
def delete_dish(
    dish_id: int = Path(..., description="ID of the dish to delete", ge=1)
):
    """
    Delete a dish from the database.
    
    Args:
        dish_id (int): ID of the dish to delete
    
    Returns:
        Response: An empty response with 204 No Content status code
    
    Raises:
        HTTPException: If the dish with the specified ID is not found
    """
    for idx, stored_dish in enumerate(dishes_db):
        if stored_dish["id"] == dish_id:
            dishes_db.pop(idx)
            return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Dish with id {dish_id} not found"
    )

# Start the application if running directly
if __name__ == "__main__":
    """
    Entry point for running the application directly.
    This will start the Uvicorn server with the FastAPI application.
    """
    import uvicorn
    uvicorn.run(
        "main:app", 
        host=settings.APP_HOST, 
        port=settings.APP_PORT, 
        reload=settings.APP_DEBUG
    )
