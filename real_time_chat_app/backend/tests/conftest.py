import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from src.database import Base, get_db
from src.main import app
from src.config import get_settings

# Test database URL (use a separate test database)
TEST_DATABASE_URL = "postgresql://postgres:password@localhost:5432/testchatapp"


# Create test engine
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Counter for unique users
_user_counter = 0


@pytest.fixture(scope="function")
def db_session():
    """Create a fresh database for each test."""
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client with test database."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()


@pytest.fixture(scope="function")
def test_user_data():
    """Generate unique user data for each test"""
    global _user_counter
    _user_counter += 1
    return {
        "username": f"testuser{_user_counter}",
        "email": f"test{_user_counter}@example.com",
        "password": "testpass123",
        "full_name": f"Test User {_user_counter}"
    }


@pytest.fixture(scope="function")
def test_user2_data():
    """Generate unique second user for each test"""
    global _user_counter
    _user_counter += 1
    return {
        "username": f"testuser{_user_counter}",
        "email": f"test{_user_counter}@example.com",
        "password": "testpass123",
        "full_name": f"Test User {_user_counter}"
    }