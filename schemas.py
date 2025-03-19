from pydantic import BaseModel, Field
from typing import Optional

class Dish(BaseModel):
    """
    Schema representing a dish in the restaurant menu.
    
    This model contains all the information needed to describe a dish,
    including its identifier, name, and price.
    
    Attributes:
        id (int): Unique identifier for the dish
        name (str): Name of the dish
        price (float): Price of the dish (must be greater than 0)
    """
    id: int = Field(
        description="Unique identifier for the dish in the database"
    )
    name: str = Field(
        description="Name of the dish"
    )
    price: float = Field(
        description="Price of the dish in local currency",
        gt=0  # Validation: price must be greater than 0
    )
    
    class Config:
        """
        Configuration class for the Dish model.
        
        This configures Pydantic behavior for this model, including ORM compatibility
        and example values for API documentation.
        """
        from_attributes = True  # For ORM compatibility (like SQLAlchemy)
        
        # Example for documentation
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Pasta Carbonara",
                "price": 12.99
            }
        }
