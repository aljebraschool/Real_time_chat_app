from sqlalchemy import Column, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class ChatRoomMember(Base):
    """
    Junction table for many-to-many relationship between users and chat rooms.
    Maps to 'chat_room_members' table.
    
    Time Complexity: O(1) for membership checks with proper indexing
    Space Complexity: O(n*m) where n=users, m=avg rooms per user
    """
    __tablename__ = "chat_room_members"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    chat_room_id = Column(
        Integer, 
        ForeignKey("chat_rooms.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    user_id = Column(
        Integer, 
        ForeignKey("users.id", ondelete="CASCADE"), 
        nullable=False,
        index=True
    )
    
    # Timestamp
    joined_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    chat_room = relationship("ChatRoom", back_populates="members")
    user = relationship("User", back_populates="chat_memberships")
    
    def __repr__(self):
        return f"<ChatRoomMember(room_id={self.chat_room_id}, user_id={self.user_id})>"