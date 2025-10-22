from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional
from src.schemas.message import MessageResponse
from typing import List as TypingList


class ChatRoomResponse(BaseModel):
    """Schema for chat room response"""
    id: int
    name: Optional[str]
    room_type: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChatRoomWithMessages(ChatRoomResponse):
    """Schema for chat room with messages"""
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True


class DirectChatResponse(BaseModel):
    """Schema for direct chat response with other user info"""
    chat_room_id: int
    other_user_id: int
    other_user_username: str
    other_user_full_name: Optional[str]
    last_message: Optional[str] = None
    last_message_time: Optional[datetime] = None
    unread_count: int = 0




class GroupCreate(BaseModel):
    """Schema for creating a group chat"""
    name: str = Field(..., min_length=1, max_length=100)
    member_ids: TypingList[int] = Field(..., min_items=1, description="List of user IDs to add")


class GroupMemberAdd(BaseModel):
    """Schema for adding members to group"""
    user_ids: TypingList[int] = Field(..., min_items=1)


class GroupMemberRemove(BaseModel):
    """Schema for removing a member from group"""
    user_id: int


class GroupResponse(BaseModel):
    """Schema for group chat response"""
    id: int
    name: str
    room_type: str
    created_by: Optional[int]
    member_count: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class GroupWithMembers(GroupResponse):
    """Schema for group with member details"""
    members: TypingList[dict] = []


class GroupMessageCreate(BaseModel):
    """Schema for sending group message"""
    group_id: int
    content: str = Field(..., min_length=1, max_length=5000)