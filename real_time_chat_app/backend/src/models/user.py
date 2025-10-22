from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    """
    User model representing registered users.
    Maps to 'users' table in database.
    
    Time Complexity: O(1) for CRUD operations with proper indexing
    Space Complexity: O(1) per user record
    """

    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key = True, index= True )

    # User credentials
    username = Column(String(225), unique = True, nullable= False, index = True )
    email = Column(String(225), unique = True, nullable = False, index = True)
    hashed_password = Column(String(255), nullable=False)

    # User info
    full_name = Column(String(225), nullable = True)
    is_active = Column(Boolean, default = True)
    is_verified = Column(Boolean, default = False)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


    # Relationships
    # One user can send many messages
    messages = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")

    # One user can create many chat rooms
    created_rooms = relationship("ChatRoom", back_populates="creator")

    # One user can be member of many chat rooms
    chat_memberships = relationship("ChatRoomMember", back_populates="user")

    # One user can have many refresh tokens
    refresh_tokens = relationship("RefreshToken", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"