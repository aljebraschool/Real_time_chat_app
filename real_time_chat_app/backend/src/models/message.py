from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class Message(Base):
    """
    Message model for storing chat messages.
    Maps to 'messages' table.
    
    Time Complexity: O(1) for insert, O(log n) for retrieval with indexing
    Space Complexity: O(n) where n=total messages
    """
    __tablename__ = "messages"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Keys
    chat_room_id = Column(Integer, ForeignKey("chat_rooms.id", ondelete="CASCADE"), nullable=False, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    
    # Message content
    content = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    
    # Relationships
    chat_room = relationship("ChatRoom", back_populates="messages")
    sender = relationship("User", back_populates="messages", foreign_keys=[sender_id])
    
    def __repr__(self):
        return f"<Message(id={self.id}, sender_id={self.sender_id}, room_id={self.chat_room_id})>"