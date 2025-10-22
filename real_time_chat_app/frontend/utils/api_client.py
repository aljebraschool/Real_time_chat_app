import requests
import streamlit as st
from typing import Optional, Dict, List


class ChatAPI:
    """
    API client for backend communication.
    """
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.token = None
    
    
    def _get_headers(self) -> Dict[str, str]:
        """Get authorization headers"""
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}
    
    
    def register(self, username: str, email: str, password: str, full_name: str = "") -> Dict:
        """Register new user"""
        url = f"{self.base_url}/auth/register"
        data = {
            "username": username,
            "email": email,
            "password": password,
            "full_name": full_name
        }
        response = requests.post(url, json=data)
        return response.json()
    
    
    def login(self, username: str, password: str) -> Dict:
        """Login user"""
        url = f"{self.base_url}/auth/login"
        data = {"username": username, "password": password}
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            result = response.json()
            self.token = result.get("tokens", {}).get("access_token")
            return result
        
        return {"error": response.json().get("detail", "Login failed")}
    
    
    def get_current_user(self) -> Dict:
        """Get current user info"""
        url = f"{self.base_url}/auth/me"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    
    def get_chats(self) -> List[Dict]:
        """Get all user's direct chats"""
        url = f"{self.base_url}/messages/chats"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    
    def get_chat_history(self, other_user_id: int, limit: int = 50) -> List[Dict]:
        """Get chat history with another user"""
        url = f"{self.base_url}/messages/chat/{other_user_id}"
        params = {"limit": limit}
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()
    
    
    def send_message(self, recipient_id: int, content: str) -> Dict:
        """Send direct message"""
        url = f"{self.base_url}/messages/send"
        data = {"recipient_id": recipient_id, "content": content}
        response = requests.post(url, json=data, headers=self._get_headers())
        return response.json()
    
    
    def get_groups(self) -> List[Dict]:
        """Get all user's groups"""
        url = f"{self.base_url}/groups/my-groups"
        response = requests.get(url, headers=self._get_headers())
        return response.json()
    
    
    def create_group(self, name: str, member_ids: List[int]) -> Dict:
        """Create group chat"""
        url = f"{self.base_url}/groups/create"
        data = {"name": name, "member_ids": member_ids}
        response = requests.post(url, json=data, headers=self._get_headers())
        return response.json()
    
    
    def send_group_message(self, group_id: int, content: str) -> Dict:
        """Send group message"""
        url = f"{self.base_url}/groups/send"
        data = {"group_id": group_id, "content": content}
        response = requests.post(url, json=data, headers=self._get_headers())
        return response.json()
    
    
    def get_group_messages(self, group_id: int, limit: int = 50) -> List[Dict]:
        """Get group messages"""
        url = f"{self.base_url}/groups/{group_id}/messages"
        params = {"limit": limit}
        response = requests.get(url, headers=self._get_headers(), params=params)
        return response.json()