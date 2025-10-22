import pytest
from fastapi.testclient import TestClient


def register_and_login(client, user_data):
    """Helper function to register and login a user"""
    client.post("/auth/register", json=user_data)
    login_response = client.post("/auth/login", json={
        "username": user_data["username"],
        "password": user_data["password"]
    })
    return login_response.json()["tokens"]["access_token"]


def test_send_direct_message(client, test_user_data, test_user2_data):
    """
    Test sending a direct message between two users.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    # Register and login both users
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    # Get user 2's ID
    user2_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token2}"}
    )
    user2_id = user2_response.json()["id"]
    
    # User 1 sends message to User 2
    message_data = {
        "recipient_id": user2_id,
        "content": "Hello from user 1!"
    }
    
    response = client.post(
        "/messages/send",
        json=message_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Message sent successfully"
    assert data["data"]["content"] == message_data["content"]


def test_send_message_to_self_fails(client, test_user_data):
    """
    Test that sending message to yourself fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    token = register_and_login(client, test_user_data)
    
    # Get own user ID
    user_response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    user_id = user_response.json()["id"]
    
    # Try to send message to self
    message_data = {
        "recipient_id": user_id,
        "content": "Message to myself"
    }
    
    response = client.post(
        "/messages/send",
        json=message_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert "yourself" in response.json()["detail"].lower()


def test_get_chat_history(client, test_user_data, test_user2_data):
    """
    Test retrieving chat history between two users.
    
    Time Complexity: O(n) where n = number of messages
    Space Complexity: O(n)
    """
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    # Get user IDs
    user1_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token1}"})
    user2_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token2}"})
    user2_id = user2_response.json()["id"]
    
    # Send messages
    client.post(
        "/messages/send",
        json={"recipient_id": user2_id, "content": "Message 1"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    client.post(
        "/messages/send",
        json={"recipient_id": user2_id, "content": "Message 2"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    # Get chat history
    response = client.get(
        f"/messages/chat/{user2_id}",
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    assert messages[0]["content"] == "Message 1"
    assert messages[1]["content"] == "Message 2"


def test_get_all_chats(client, test_user_data, test_user2_data):
    """
    Test getting all user's chats.
    
    Time Complexity: O(n) where n = number of chats
    Space Complexity: O(n)
    """
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    # Get user 2 ID
    user2_response = client.get("/auth/me", headers={"Authorization": f"Bearer {token2}"})
    user2_id = user2_response.json()["id"]
    
    # Send a message to create chat
    client.post(
        "/messages/send",
        json={"recipient_id": user2_id, "content": "Hi!"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    # Get all chats for user 1
    response = client.get(
        "/messages/chats",
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 200
    chats = response.json()
    assert len(chats) == 1
    assert chats[0]["other_user_id"] == user2_id


def test_unauthorized_send_message(client, test_user_data):
    """
    Test sending message without authentication fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    response = client.post(
        "/messages/send",
        json={"recipient_id": 999, "content": "Test"}
    )
    
    assert response.status_code == 403


def test_send_message_to_nonexistent_user(client, test_user_data):
    """
    Test sending message to non-existent user fails.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    token = register_and_login(client, test_user_data)
    
    response = client.post(
        "/messages/send",
        json={"recipient_id": 99999, "content": "Hello"},
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()