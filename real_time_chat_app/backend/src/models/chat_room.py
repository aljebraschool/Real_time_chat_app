from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from src.database import Base

class RoomType(str, enum.Enum):
    """Enum for chat room type"""
    DIRECT = "direct" #1-to-1 chat
    GROUP = "group" #group chat


class ChatRoom(Base):
    """
    ChatRoom model for both direct and group chats.
    Maps to 'chat_rooms' table.
    
    Direct chat: room_type='direct', name=None, 2 members
    Group chat: room_type='group', name='Family', 2+ members
    
    Time Complexity: O(1) for CRUD operations
    Space Complexity: O(1) per room
    """

    __tablename__ = "chat_rooms"

    # Primary Key
    id = Column(Integer, primary_key=True, index = True)

    # Room details
    name = Column(String(225), nullable = True)
    # room_type = Column(Enum(RoomType), nullable = False)
    room_type = Column(String(20), nullable=False)

    # Foreign Key
    created_by = Column(Integer, ForeignKey("users.id", ondelete= "SET NULL"), nullable=True )


    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    # Relationships
    # One room has one creator
    creator = relationship("User", back_populates="created_rooms")

    # One room has many messages
    messages = relationship("Message", back_populates="chat_room", cascade="all, delete-orphan")

    # One room has many members
    members = relationship("ChatRoomMember", back_populates="chat_room", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<ChatRoom(id={self.id}, type='{self.room_type}', name='{self.name}')>"

