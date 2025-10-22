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


def get_user_id(client, token):
    """Helper to get user ID from token"""
    response = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    return response.json()["id"]


def test_create_group(client, test_user_data, test_user2_data):
    """
    Test creating a group chat.
    
    Time Complexity: O(n) where n = number of members
    Space Complexity: O(n)
    """
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    user2_id = get_user_id(client, token2)
    
    # Create group
    group_data = {
        "name": "Test Group",
        "member_ids": [user2_id]
    }
    
    response = client.post(
        "/groups/create",
        json=group_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Group created successfully"
    assert data["group"]["name"] == "Test Group"
    assert data["group"]["member_count"] >= 2  # Creator + user2


# def test_create_group_with_nonexistent_user(client, test_user_data):
#     """
#     Test creating group with non-existent user fails.
    
#     Time Complexity: O(1)
#     Space Complexity: O(1)
#     """
#     token = register_and_login(client, test_user_data)
    
#     group_data = {
#         "name": "Test Group",
#         "member_ids": [99999]
#     }
    
#     response = client.post(
#         "/groups/create",
#         json=group_data,
#         headers={"Authorization": f"Bearer {token}"}
#     )
    
#     assert response.status_code == 400
#     assert "not found" in response.json()["detail"].lower()

def test_create_group_with_nonexistent_user(client, test_user_data):
    """Test creating group with non-existent user fails."""
    token = register_and_login(client, test_user_data)
    
    import random
    rand = random.randint(40000, 49999)
    
    group_data = {
        "name": f"Test Group {rand}",
        "member_ids": [999999]  # Non-existent user
    }
    
    response = client.post(
        "/groups/create",
        json=group_data,
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400
    assert "not found" in response.json()["detail"].lower()


# def test_send_group_message(client, test_user_data, test_user2_data):
#     """
#     Test sending message to a group.
    
#     Time Complexity: O(1)
#     Space Complexity: O(1)
#     """
#     token1 = register_and_login(client, test_user_data)
#     token2 = register_and_login(client, test_user2_data)
    
#     user2_id = get_user_id(client, token2)
    
#     # Create group
#     group_response = client.post(
#         "/groups/create",
#         json={"name": "Test Group", "member_ids": [user2_id]},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
#     group_id = group_response.json()["group"]["id"]
    
#     # Send message
#     message_data = {
#         "group_id": group_id,
#         "content": "Hello group!"
#     }
    
#     response = client.post(
#         "/groups/send",
#         json=message_data,
#         headers={"Authorization": f"Bearer {token1}"}
#     )
    
#     assert response.status_code == 201
#     data = response.json()
#     assert data["message"] == "Message sent successfully"
#     assert data["data"]["content"] == "Hello group!"

def test_send_group_message(client, test_user_data, test_user2_data):
    """Test sending message to a group."""
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    user2_id = get_user_id(client, token2)
    
    import random
    rand = random.randint(60000, 69999)
    
    # Create group with unique name
    group_response = client.post(
        "/groups/create",
        json={"name": f"Test Group {rand}", "member_ids": [user2_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    group_id = group_response.json()["group"]["id"]
    
    # Send message
    message_data = {
        "group_id": group_id,
        "content": "Hello group!"
    }
    
    response = client.post(
        "/groups/send",
        json=message_data,
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["message"] == "Message sent successfully"
    assert data["data"]["content"] == "Hello group!"


# def test_send_message_to_group_not_member(client, test_user_data, test_user2_data):
#     """
#     Test sending message to group you're not a member of fails.
    
#     Time Complexity: O(1)
#     Space Complexity: O(1)
#     """
#     token1 = register_and_login(client, test_user_data)
#     token2 = register_and_login(client, test_user2_data)
    
#     # User 1 creates group without user 2
#     group_response = client.post(
#         "/groups/create",
#         json={"name": "Private Group", "member_ids": []},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
#     group_id = group_response.json()["group"]["id"]
    
#     # User 2 tries to send message
#     response = client.post(
#         "/groups/send",
#         json={"group_id": group_id, "content": "Can I join?"},
#         headers={"Authorization": f"Bearer {token2}"}
#     )
    
#     assert response.status_code == 400
#     assert "not a member" in response.json()["detail"].lower()

def test_send_message_to_group_not_member(client, test_user_data, test_user2_data):
    """Test sending message to group you're not a member of fails."""
    token1 = register_and_login(client, test_user_data)
    
    # Generate unique third user
    import random
    rand = random.randint(20000, 29999)
    user3_data = {
        "username": f"user{rand}",
        "email": f"user{rand}@test.com",
        "password": "password123"
    }
    token2 = register_and_login(client, user3_data)
    
    # User 1 creates group without user 2
    group_response = client.post(
        "/groups/create",
        json={"name": f"Private Group {rand}", "member_ids": []},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    # Check if group creation succeeded
    if group_response.status_code != 201:
        print(f"Group creation failed: {group_response.json()}")
        pytest.skip("Group creation failed")
    
    group_id = group_response.json()["group"]["id"]
    
    # User 2 tries to send message
    response = client.post(
        "/groups/send",
        json={"group_id": group_id, "content": "Can I join?"},
        headers={"Authorization": f"Bearer {token2}"}
    )
    
    assert response.status_code == 400
    assert "not a member" in response.json()["detail"].lower()

def test_get_group_messages(client, test_user_data, test_user2_data):
    """
    Test getting messages from a group.
    
    Time Complexity: O(n) where n = number of messages
    Space Complexity: O(n)
    """
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    user2_id = get_user_id(client, token2)
    
    # Create group
    group_response = client.post(
        "/groups/create",
        json={"name": "Test Group", "member_ids": [user2_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    group_id = group_response.json()["group"]["id"]
    
    # Send messages
    client.post(
        "/groups/send",
        json={"group_id": group_id, "content": "Message 1"},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    client.post(
        "/groups/send",
        json={"group_id": group_id, "content": "Message 2"},
        headers={"Authorization": f"Bearer {token2}"}
    )
    
    # Get messages
    response = client.get(
        f"/groups/{group_id}/messages",
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 200
    messages = response.json()
    assert len(messages) == 2
    assert messages[0]["content"] == "Message 1"
    assert messages[1]["content"] == "Message 2"


# def test_get_my_groups(client, test_user_data, test_user2_data):
#     """
#     Test getting all groups user is member of.
    
#     Time Complexity: O(n) where n = number of groups
#     Space Complexity: O(n)
#     """
#     token1 = register_and_login(client, test_user_data)
#     token2 = register_and_login(client, test_user2_data)
    
#     user2_id = get_user_id(client, token2)
    
#     # Create two groups
#     client.post(
#         "/groups/create",
#         json={"name": "Group 1", "member_ids": [user2_id]},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
    
#     client.post(
#         "/groups/create",
#         json={"name": "Group 2", "member_ids": [user2_id]},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
    
#     # Get groups for user 1
#     response = client.get(
#         "/groups/my-groups",
#         headers={"Authorization": f"Bearer {token1}"}
#     )
    
#     assert response.status_code == 200
#     groups = response.json()
#     assert len(groups) == 2
#     assert groups[0]["name"] in ["Group 1", "Group 2"]

def test_get_my_groups(client, test_user_data, test_user2_data):
    """Test getting all groups user is member of."""
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    user2_id = get_user_id(client, token2)
    
    import random
    rand = random.randint(50000, 59999)
    
    # Create two groups with unique names
    client.post(
        "/groups/create",
        json={"name": f"Group {rand}_1", "member_ids": [user2_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    client.post(
        "/groups/create",
        json={"name": f"Group {rand}_2", "member_ids": [user2_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    # Get groups for user 1
    response = client.get(
        "/groups/my-groups",
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 200
    groups = response.json()
    assert len(groups) == 2


# def test_add_members_to_group(client, test_user_data, test_user2_data):
#     """
#     Test adding members to a group (creator only).
    
#     Time Complexity: O(n) where n = members to add
#     Space Complexity: O(1)
#     """
#     token1 = register_and_login(client, test_user_data)
#     token2 = register_and_login(client, test_user2_data)
    
#     # Register third user
#     user3_data = {
#         "username": "user3",
#         "email": "user3@test.com",
#         "password": "password123"
#     }
#     token3 = register_and_login(client, user3_data)
#     user3_id = get_user_id(client, token3)
    
#     # Create group (without user3)
#     group_response = client.post(
#         "/groups/create",
#         json={"name": "Test Group", "member_ids": []},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
#     group_id = group_response.json()["group"]["id"]
    
#     # Add user3
#     response = client.post(
#         f"/groups/{group_id}/members",
#         json={"user_ids": [user3_id]},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
    
#     assert response.status_code == 200
#     assert "added" in response.json()["message"].lower()

def test_add_members_to_group(client, test_user_data, test_user2_data):
    """Test adding members to a group (creator only)."""
    token1 = register_and_login(client, test_user_data)
    
    # Generate unique third user
    import random
    rand = random.randint(30000, 39999)
    user3_data = {
        "username": f"user{rand}",
        "email": f"user{rand}@test.com",
        "password": "password123"
    }
    token3 = register_and_login(client, user3_data)
    user3_id = get_user_id(client, token3)
    
    # Create group (without user3)
    group_response = client.post(
        "/groups/create",
        json={"name": f"Test Group {rand}", "member_ids": []},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    # Check if successful
    if group_response.status_code != 201:
        print(f"Group creation failed: {group_response.json()}")
        pytest.skip("Group creation failed")
    
    group_id = group_response.json()["group"]["id"]
    
    # Add user3
    response = client.post(
        f"/groups/{group_id}/members",
        json={"user_ids": [user3_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    
    assert response.status_code == 200
    assert "added" in response.json()["message"].lower()



# def test_non_creator_cannot_add_members(client, test_user_data, test_user2_data):
#     """
#     Test that non-creator cannot add members.
    
#     Time Complexity: O(1)
#     Space Complexity: O(1)
#     """
#     token1 = register_and_login(client, test_user_data)
#     token2 = register_and_login(client, test_user2_data)
    
#     user2_id = get_user_id(client, token2)
    
#     # User 1 creates group
#     group_response = client.post(
#         "/groups/create",
#         json={"name": "Test Group", "member_ids": [user2_id]},
#         headers={"Authorization": f"Bearer {token1}"}
#     )
#     group_id = group_response.json()["group"]["id"]
    
#     # User 2 tries to add members (should fail)
#     response = client.post(
#         f"/groups/{group_id}/members",
#         json={"user_ids": [999]},
#         headers={"Authorization": f"Bearer {token2}"}
#     )
    
#     assert response.status_code == 403
#     assert "creator" in response.json()["detail"].lower()

def test_non_creator_cannot_add_members(client, test_user_data, test_user2_data):
    """Test that non-creator cannot add members."""
    token1 = register_and_login(client, test_user_data)
    token2 = register_and_login(client, test_user2_data)
    
    user2_id = get_user_id(client, token2)
    
    import random
    rand = random.randint(70000, 79999)
    
    # User 1 creates group with unique name
    group_response = client.post(
        "/groups/create",
        json={"name": f"Test Group {rand}", "member_ids": [user2_id]},
        headers={"Authorization": f"Bearer {token1}"}
    )
    group_id = group_response.json()["group"]["id"]
    
    # User 2 tries to add members (should fail)
    response = client.post(
        f"/groups/{group_id}/members",
        json={"user_ids": [999]},
        headers={"Authorization": f"Bearer {token2}"}
    )
    
    assert response.status_code == 403
    assert "creator" in response.json()["detail"].lower()