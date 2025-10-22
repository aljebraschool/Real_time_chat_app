from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, Query
from sqlalchemy.orm import Session
from src.database import get_db
from src.services.websocket_manager import manager
from src.services.chat_service import ChatService
from src.services.auth_service import AuthService
from src.repositories.chat_repository import ChatRepository
from src.repositories.user_repository import UserRepository
import json

router = APIRouter(tags=["WebSocket"])


@router.websocket("/ws/{token}")
async def websocket_endpoint(
    websocket: WebSocket,
    token: str,
    db: Session = Depends(get_db)
):
    """
    WebSocket endpoint for real-time chat.
    
    Connection URL: ws://localhost:8000/ws/{access_token}
    
    Message formats:
    
    1. Join room:
       {"type": "join_room", "room_id": 1}
    
    2. Leave room:
       {"type": "leave_room", "room_id": 1}
    
    3. Send message:
       {"type": "message", "room_id": 1, "content": "Hello!"}
    
    4. Typing indicator:
       {"type": "typing", "room_id": 1}
    
    Time Complexity: O(1) for connection, O(n) for broadcasts
    Space Complexity: O(1)
    """
    
    # Authenticate user from token
    user = AuthService.get_current_user(db, token)
    
    if not user:
        await websocket.close(code=4001, reason="Invalid token")
        return
    
    user_id = user.id
    
    # Connect user
    await manager.connect(user_id, websocket)
    
    try:
        # Send connection confirmation
        await websocket.send_json({
            "type": "connected",
            "user_id": user_id,
            "username": user.username,
            "message": "Connected to chat server"
        })
        
        # Listen for messages
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            message_type = message_data.get("type")
            
            # Handle different message types
            if message_type == "join_room":
                # Join a chat room
                room_id = message_data.get("room_id")
                
                # Verify user has access to room
                if ChatRepository.is_user_in_chat(db, user_id, room_id):
                    manager.join_room(user_id, room_id)
                    
                    # Notify user
                    await manager.send_personal_message(user_id, {
                        "type": "room_joined",
                        "room_id": room_id,
                        "message": f"Joined room {room_id}"
                    })
                    
                    # Notify others in room
                    await manager.broadcast_to_room(room_id, {
                        "type": "user_joined",
                        "room_id": room_id,
                        "user_id": user_id,
                        "username": user.username
                    }, exclude_user=user_id)
                else:
                    await manager.send_personal_message(user_id, {
                        "type": "error",
                        "message": "You don't have access to this room"
                    })
            
            elif message_type == "leave_room":
                # Leave a chat room
                room_id = message_data.get("room_id")
                manager.leave_room(user_id, room_id)
                
                # Notify user
                await manager.send_personal_message(user_id, {
                    "type": "room_left",
                    "room_id": room_id,
                    "message": f"Left room {room_id}"
                })
                
                # Notify others
                await manager.broadcast_to_room(room_id, {
                    "type": "user_left",
                    "room_id": room_id,
                    "user_id": user_id,
                    "username": user.username
                })
            
            elif message_type == "message":
                # Send a message to room
                room_id = message_data.get("room_id")
                content = message_data.get("content")
                
                if not content or not content.strip():
                    continue
                
                # Verify user is in room
                if not ChatRepository.is_user_in_chat(db, user_id, room_id):
                    await manager.send_personal_message(user_id, {
                        "type": "error",
                        "message": "You are not in this room"
                    })
                    continue
                
                # Save message to database
                message = ChatRepository.create_message(db, room_id, user_id, content)
                
                # Broadcast to all users in room
                await manager.broadcast_to_room(room_id, {
                    "type": "new_message",
                    "room_id": room_id,
                    "message_id": message.id,
                    "sender_id": user_id,
                    "sender_username": user.username,
                    "sender_full_name": user.full_name,
                    "content": content,
                    "created_at": str(message.created_at)
                })
            
            elif message_type == "typing":
                # Typing indicator
                room_id = message_data.get("room_id")
                
                # Broadcast to others in room (exclude sender)
                await manager.broadcast_to_room(room_id, {
                    "type": "user_typing",
                    "room_id": room_id,
                    "user_id": user_id,
                    "username": user.username
                }, exclude_user=user_id)
            
            elif message_type == "ping":
                # Keep-alive ping
                await manager.send_personal_message(user_id, {
                    "type": "pong"
                })
            
            else:
                # Unknown message type
                await manager.send_personal_message(user_id, {
                    "type": "error",
                    "message": f"Unknown message type: {message_type}"
                })
    
    except WebSocketDisconnect:
        # User disconnected
        manager.disconnect(user_id)
        print(f"User {user_id} disconnected")
    
    except Exception as e:
        # Error occurred
        print(f"WebSocket error for user {user_id}: {e}")
        manager.disconnect(user_id)


@router.get("/ws/online-users")
async def get_online_users():
    """
    Get list of currently online users.
    
    Time Complexity: O(n)
    Space Complexity: O(n)
    """
    return {
        "online_users": manager.get_online_users(),
        "count": len(manager.get_online_users())
    }