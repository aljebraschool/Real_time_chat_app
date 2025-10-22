import pytest
from fastapi.testclient import TestClient


def test_register_user(client, test_user_data):
    """
    Test user registration.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    response = client.post("/auth/register", json=test_user_data)
    
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "user" in data
    assert data["user"]["username"] == test_user_data["username"]
    assert data["user"]["email"] == test_user_data["email"]
    assert "tokens" in data


def test_register_duplicate_username(client, test_user_data):
    """
    Test registration with duplicate username fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register first user
    client.post("/auth/register", json=test_user_data)
    
    # Try to register same username again
    response = client.post("/auth/register", json=test_user_data)
    
    assert response.status_code == 400
    assert "already taken" in response.json()["detail"].lower()


def test_login_success(client, test_user_data):
    """
    Test successful login.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register user first
    client.post("/auth/register", json=test_user_data)
    
    # Login
    login_data = {
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "tokens" in data
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]


def test_login_wrong_password(client, test_user_data):
    """
    Test login with wrong password fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register user
    client.post("/auth/register", json=test_user_data)
    
    # Try wrong password
    login_data = {
        "username": test_user_data["username"],
        "password": "wrongpassword"
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401


def test_login_nonexistent_user(client):
    """
    Test login with non-existent user fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    login_data = {
        "username": "nonexistent",
        "password": "password123"
    }
    response = client.post("/auth/login", json=login_data)
    
    assert response.status_code == 401


def test_get_current_user(client, test_user_data):
    """
    Test getting current user info with valid token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    
    token = login_response.json()["tokens"]["access_token"]
    
    # Get current user
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user_data["username"]


def test_get_current_user_invalid_token(client):
    """
    Test getting current user with invalid token fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    assert response.status_code == 401


def test_refresh_token(client, test_user_data):
    """
    Test refreshing access token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    
    refresh_token = login_response.json()["tokens"]["refresh_token"]
    
    # Refresh token
    response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data


def test_logout(client, test_user_data):
    """
    Test logout functionality.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register and login
    client.post("/auth/register", json=test_user_data)
    login_response = client.post("/auth/login", json={
        "username": test_user_data["username"],
        "password": test_user_data["password"]
    })
    
    refresh_token = login_response.json()["tokens"]["refresh_token"]
    
    # Logout
    response = client.post("/auth/logout", json={"refresh_token": refresh_token})
    
    assert response.status_code == 200
    
    # Try to use refresh token again (should fail)
    refresh_response = client.post("/auth/refresh", json={"refresh_token": refresh_token})
    assert refresh_response.status_code == 401