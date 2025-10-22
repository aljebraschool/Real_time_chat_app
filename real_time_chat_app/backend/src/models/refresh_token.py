from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.database import Base


class RefreshToken(Base):
    """
    RefreshToken model for storing JWT refresh tokens.
    Maps to 'refresh_tokens' table.
    
    Used for maintaining user sessions securely.
    
    Time Complexity: O(1) for token lookup with unique index
    Space Complexity: O(n) where n=active sessions
    """
    __tablename__ = "refresh_tokens"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Token data
    token = Column(String(500), unique=True, nullable=False, index=True)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    
    # Timestamp
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationship
    user = relationship("User", back_populates="refresh_tokens")
    
    def __repr__(self):
        return f"<RefreshToken(id={self.id}, user_id={self.user_id})>"