import os
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseModel):
    """
    Application settings configuration.
    
    This class handles all configuration settings for the application,
    loading values from environment variables with sensible defaults.
    
    Attributes:
        APP_TITLE (str): The title of the application
        APP_DESCRIPTION (str): A description of the application
        APP_VERSION (str): The version of the application
        APP_HOST (str): The host to bind the server to
        APP_PORT (int): The port to bind the server to
        APP_DEBUG (bool): Whether to run the application in debug mode
    """
    # Application information
    APP_TITLE: str = "Dish Management API"
    APP_DESCRIPTION: str = "An API for managing restaurant dishes"
    APP_VERSION: str = "0.1.0"
    
    # Server configuration
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    APP_DEBUG: bool = os.getenv("APP_DEBUG", "true").lower() == "true"
    
    # Other configurations can be added here
    # DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    
    model_config = {
        "env_file": ".env"
    }


# Create a settings instance to import in other files
settings = Settings()
