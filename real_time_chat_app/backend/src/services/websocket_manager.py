from typing import Dict, List, Set
from fastapi import WebSocket
import json
from datetime import datetime


class ConnectionManager:
    """
    Manages WebSocket connections for real-time chat.
    
    Structure:
    - active_connections: {user_id: WebSocket}
    - room_connections: {room_id: {user_id1, user_id2, ...}}
    """
    
    def __init__(self):
        """
        Initialize connection manager.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        """
        # Map user_id to their WebSocket connection
        self.active_connections: Dict[int, WebSocket] = {}
        
        # Map room_id to set of user_ids in that room
        self.room_connections: Dict[int, Set[int]] = {}
    
    
    async def connect(self, user_id: int, websocket: WebSocket):
        """
        Connect a user via WebSocket.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            user_id: User ID
            websocket: WebSocket connection
        """
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ User {user_id} connected via WebSocket")
    
    
    def disconnect(self, user_id: int):
        """
        Disconnect a user.
        
        Time Complexity: O(n) where n = number of rooms user is in
        Space Complexity: O(1)
        
        Args:
            user_id: User ID
        """
        # Remove from active connections
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Remove from all rooms
        for room_id in list(self.room_connections.keys()):
            if user_id in self.room_connections[room_id]:
                self.room_connections[room_id].remove(user_id)
                
                # Remove room if empty
                if not self.room_connections[room_id]:
                    del self.room_connections[room_id]
        
        print(f"❌ User {user_id} disconnected")
    
    
    def join_room(self, user_id: int, room_id: int):
        """
        Add user to a chat room.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            user_id: User ID
            room_id: Room ID
        """
        if room_id not in self.room_connections:
            self.room_connections[room_id] = set()
        
        self.room_connections[room_id].add(user_id)
        print(f"👥 User {user_id} joined room {room_id}")
    
    
    def leave_room(self, user_id: int, room_id: int):
        """
        Remove user from a chat room.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            user_id: User ID
            room_id: Room ID
        """
        if room_id in self.room_connections:
            self.room_connections[room_id].discard(user_id)
            
            # Remove room if empty
            if not self.room_connections[room_id]:
                del self.room_connections[room_id]
        
        print(f"🚪 User {user_id} left room {room_id}")
    
    
    async def send_personal_message(self, user_id: int, message: dict):
        """
        Send message to a specific user.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            user_id: User ID to send to
            message: Message dictionary
        """
        if user_id in self.active_connections:
            websocket = self.active_connections[user_id]
            try:
                await websocket.send_json(message)
            except Exception as e:
                print(f"❌ Error sending to user {user_id}: {e}")
                self.disconnect(user_id)
    
    
    async def broadcast_to_room(self, room_id: int, message: dict, exclude_user: int = None):
        """
        Send message to all users in a room.
        
        Time Complexity: O(n) where n = users in room
        Space Complexity: O(1)
        
        Args:
            room_id: Room ID
            message: Message dictionary
            exclude_user: Optional user ID to exclude (e.g., sender)
        """
        if room_id not in self.room_connections:
            return
        
        disconnected_users = []
        
        for user_id in self.room_connections[room_id]:
            # Skip excluded user
            if exclude_user and user_id == exclude_user:
                continue
            
            # Send to user if connected
            if user_id in self.active_connections:
                websocket = self.active_connections[user_id]
                try:
                    await websocket.send_json(message)
                except Exception as e:
                    print(f"❌ Error broadcasting to user {user_id}: {e}")
                    disconnected_users.append(user_id)
        
        # Clean up disconnected users
        for user_id in disconnected_users:
            self.disconnect(user_id)
    
    
    def get_online_users(self) -> List[int]:
        """
        Get list of all online user IDs.
        
        Time Complexity: O(n) where n = connected users
        Space Complexity: O(n)
        
        Returns:
            List of user IDs
        """
        return list(self.active_connections.keys())
    
    
    def is_user_online(self, user_id: int) -> bool:
        """
        Check if user is online.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            user_id: User ID
            
        Returns:
            True if online, False otherwise
        """
        return user_id in self.active_connections


# Global connection manager instance
manager = ConnectionManager()