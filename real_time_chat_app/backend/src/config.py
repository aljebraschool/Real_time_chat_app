# from pydantic_settings import BaseSettings
# from functools import lru_cache


# class Settings(BaseSettings):
#     """
#     Application settings loaded from environment variables.
#     Uses pydantic for validations and type safety
#     """

#     #Database
#     DATABASE_URL : str

#     #JWT Authentication
#     SECRET_KEY : str
#     ALGORITHM : str = "HS256"
#     ACCESS_TOKEN_EXPIRE_MINUTES : int = 30
#     REFRESH_TOKEN_EXPIRE_DAYS : int = 7

#     #App Settings
#     DEBUG : bool = True
#     APP_NAME : str = "RealTimeChatApp"

#     class Config:
#         env_file = ".env"
#         case_sensitive = True 

    
# @lru_cache
# def get_settings() -> Settings:
#     """
#     Returns cached settings instance.
#     lru_cache ensures we only load .env once.
    
#     Time Complexity: O(1)
#     Space Complexity: O(1)
#     """
#     return Settings()


from pydantic_settings import BaseSettings
from functools import lru_cache
import os
from pathlib import Path

# Get the project root directory (2 levels up from this file)
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE = BASE_DIR / ".env"


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.
    """
    # Database
    DATABASE_URL: str
    
    # JWT Authentication
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # App Settings
    DEBUG: bool = True
    APP_NAME: str = "RealtimeChatApp"
    
    class Config:
        env_file = str(ENV_FILE)
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """
    Returns cached settings instance.
    """
    return Settings()