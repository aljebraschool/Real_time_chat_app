import sys
sys.path.append('backend')

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.config import get_settings

settings = get_settings()

# Create database engine
# pool_pre_ping=True checks connection health before using
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# Session factory for database operations
SessionLocal = sessionmaker(autoflush=False, autocommit = False, bind=engine)

# Base class for all models
Base = declarative_base()

def get_db():
    """
    Dependency function that provides database session to routes.
    Automatically closes session after request.
    
    Usage:
        @app.get("/users")
        def get_users(db: Session = Depends(get_db)):
            ...
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    