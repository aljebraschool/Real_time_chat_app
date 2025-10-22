from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional
from src.models.user import User
from src.models.refresh_token import RefreshToken
from datetime import datetime


class UserRepository:
    """
    Repository for User database operations.
    Handles all user-related CRUD operations.
    """
    
    @staticmethod
    def create_user(db: Session, username: str, email: str, hashed_password: str, 
                    full_name: Optional[str] = None) -> User:
        """
        Create a new user in database.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            username: Unique username
            email: User email
            hashed_password: Already hashed password
            full_name: Optional full name
            
        Returns:
            Created User object
        """
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password,
            full_name=full_name
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
        """
        Get user by ID.
        
        Time Complexity: O(1) with primary key index
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object or None
        """
        return db.query(User).filter(User.id == user_id).first()
    
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[User]:
        """
        Get user by username.
        
        Time Complexity: O(1) with username index
        Space Complexity: O(1)
        
        Args:
            db: Database session
            username: Username
            
        Returns:
            User object or None
        """
        return db.query(User).filter(User.username == username).first()
    
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """
        Get user by email.
        
        Time Complexity: O(1) with email index
        Space Complexity: O(1)
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User object or None
        """
        return db.query(User).filter(User.email == email).first()
    
    
    @staticmethod
    def get_user_by_username_or_email(db: Session, identifier: str) -> Optional[User]:
        """
        Get user by username OR email (for login).
        
        Time Complexity: O(1) with indexes
        Space Complexity: O(1)
        
        Args:
            db: Database session
            identifier: Username or email
            
        Returns:
            User object or None
        """
        return db.query(User).filter(
            or_(User.username == identifier, User.email == identifier)
        ).first()
    
    
    @staticmethod
    def update_user_password(db: Session, user_id: int, hashed_password: str) -> Optional[User]:
        """
        Update user password.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            hashed_password: New hashed password
            
        Returns:
            Updated User object or None
        """
        user = UserRepository.get_user_by_id(db, user_id)
        if user:
            user.hashed_password = hashed_password
            db.commit()
            db.refresh(user)
        return user
    
    
    @staticmethod
    def save_refresh_token(db: Session, user_id: int, token: str, expires_at: datetime) -> RefreshToken:
        """
        Save refresh token to database.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            token: Refresh token string
            expires_at: Token expiration datetime
            
        Returns:
            Created RefreshToken object
        """
        refresh_token = RefreshToken(
            user_id=user_id,
            token=token,
            expires_at=expires_at
        )
        db.add(refresh_token)
        db.commit()
        db.refresh(refresh_token)
        return refresh_token
    
    
    @staticmethod
    def get_refresh_token(db: Session, token: str) -> Optional[RefreshToken]:
        """
        Get refresh token from database.
        
        Time Complexity: O(1) with token unique index
        Space Complexity: O(1)
        
        Args:
            db: Database session
            token: Refresh token string
            
        Returns:
            RefreshToken object or None
        """
        return db.query(RefreshToken).filter(RefreshToken.token == token).first()
    
    
    @staticmethod
    def delete_refresh_token(db: Session, token: str) -> bool:
        """
        Delete refresh token (for logout).
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            token: Refresh token string
            
        Returns:
            True if deleted, False if not found
        """
        refresh_token = UserRepository.get_refresh_token(db, token)
        if refresh_token:
            db.delete(refresh_token)
            db.commit()
            return True
        return False
    
    
    @staticmethod
    def delete_user_refresh_tokens(db: Session, user_id: int) -> int:
        """
        Delete all refresh tokens for a user (logout from all devices).
        
        Time Complexity: O(n) where n is number of user's tokens
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Number of tokens deleted
        """
        deleted = db.query(RefreshToken).filter(RefreshToken.user_id == user_id).delete()
        db.commit()
        return deleted