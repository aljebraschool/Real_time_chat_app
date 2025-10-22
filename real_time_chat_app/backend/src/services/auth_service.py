from sqlalchemy.orm import Session
from datetime import datetime, timedelta, timezone
from typing import Optional, Tuple
from src.repositories.user_repository import UserRepository
from src.schemas.auth import UserRegister, UserLogin, TokenResponse
from src.schemas.user import UserResponse
from src.utils.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    create_refresh_token,
    verify_token
)
from src.models.user import User
from src.config import get_settings

settings = get_settings()


class AuthService:
    """
    Authentication service containing business logic.
    Coordinates between repositories and security utilities.
    """
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> Tuple[UserResponse, TokenResponse]:
        """
        Register a new user.
        
        Time Complexity: O(1) for database operations
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Tuple of (UserResponse, TokenResponse)
            
        Raises:
            ValueError: If username or email already exists
        """
        # Check if username exists
        existing_user = UserRepository.get_user_by_username(db, user_data.username)
        if existing_user:
            raise ValueError("Username already taken")
        
        # Check if email exists
        existing_email = UserRepository.get_user_by_email(db, user_data.email)
        if existing_email:
            raise ValueError("Email already registered")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create user
        user = UserRepository.create_user(
            db=db,
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name
        )
        
        # Generate tokens
        tokens = AuthService._generate_tokens(db, user)
        
        # Convert to response schema
        user_response = UserResponse.model_validate(user)
        
        return user_response, tokens
    
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> Tuple[UserResponse, TokenResponse]:
        """
        Authenticate user and generate tokens.
        
        Time Complexity: O(1) for database lookup + O(n) for password verification
        Space Complexity: O(1)
        
        Args:
            db: Database session
            login_data: User login credentials
            
        Returns:
            Tuple of (UserResponse, TokenResponse)
            
        Raises:
            ValueError: If credentials are invalid
        """
        # Find user by username or email
        user = UserRepository.get_user_by_username_or_email(db, login_data.username)
        
        if not user:
            raise ValueError("Invalid username or password")
        
        # Verify password
        if not verify_password(login_data.password, user.hashed_password):
            raise ValueError("Invalid username or password")
        
        # Check if user is active
        if not user.is_active:
            raise ValueError("Account is inactive")
        
        # Generate tokens
        tokens = AuthService._generate_tokens(db, user)
        
        # Convert to response schema
        user_response = UserResponse.model_validate(user)
        
        return user_response, tokens
    
    
    @staticmethod
    def refresh_access_token(db: Session, refresh_token: str) -> TokenResponse:
        """
        Generate new access token using refresh token.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            refresh_token: Refresh token string
            
        Returns:
            New TokenResponse with fresh access token
            
        Raises:
            ValueError: If refresh token is invalid or expired
        """
        # Verify refresh token
        payload = verify_token(refresh_token, token_type="refresh")
        if not payload:
            raise ValueError("Invalid refresh token")
        
        # Check if token exists in database
        db_token = UserRepository.get_refresh_token(db, refresh_token)
        if not db_token:
            raise ValueError("Refresh token not found")
        
        # Check if token is expired
        if db_token.expires_at.replace(tzinfo=None) < datetime.utcnow():
            # Delete expired token
            UserRepository.delete_refresh_token(db, refresh_token)
            raise ValueError("Refresh token expired")
        
        # Get user
        user_id = int(payload.get("sub"))
        user = UserRepository.get_user_by_id(db, user_id)
        
        if not user or not user.is_active:
            raise ValueError("User not found or inactive")
        
        # Generate new access token (keep same refresh token)
        access_token = create_access_token({"sub": str(user.id)})
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )
    
    
    @staticmethod
    def logout_user(db: Session, refresh_token: str) -> bool:
        """
        Logout user by deleting refresh token.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            refresh_token: Refresh token to delete
            
        Returns:
            True if successful, False otherwise
        """
        return UserRepository.delete_refresh_token(db, refresh_token)
    
    
    @staticmethod
    def logout_all_devices(db: Session, user_id: int) -> int:
        """
        Logout user from all devices.
        
        Time Complexity: O(n) where n is number of user's tokens
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Number of sessions terminated
        """
        return UserRepository.delete_user_refresh_tokens(db, user_id)
    
    
    @staticmethod
    def change_password(db: Session, user_id: int, old_password: str, new_password: str) -> bool:
        """
        Change user password.
        
        Time Complexity: O(1) + O(n) for password hashing
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            old_password: Current password
            new_password: New password
            
        Returns:
            True if successful
            
        Raises:
            ValueError: If old password is incorrect
        """
        # Get user
        user = UserRepository.get_user_by_id(db, user_id)
        if not user:
            raise ValueError("User not found")
        
        # Verify old password
        if not verify_password(old_password, user.hashed_password):
            raise ValueError("Current password is incorrect")
        
        # Hash new password
        hashed_password = hash_password(new_password)
        
        # Update password
        UserRepository.update_user_password(db, user_id, hashed_password)
        
        # Logout from all devices for security
        AuthService.logout_all_devices(db, user_id)
        
        return True
    
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> Optional[User]:
        """
        Get current user from access token.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            token: Access token
            
        Returns:
            User object or None
        """
        # Verify token
        payload = verify_token(token, token_type="access")
        if not payload:
            return None
        
        # Get user
        user_id = int(payload.get("sub"))
        user = UserRepository.get_user_by_id(db, user_id)
        
        if not user or not user.is_active:
            return None
        
        return user
    
    
    @staticmethod
    def _generate_tokens(db: Session, user: User) -> TokenResponse:
        """
        Generate access and refresh tokens for user.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user: User object
            
        Returns:
            TokenResponse with both tokens
        """
        # Create access token
        access_token = create_access_token({"sub": str(user.id)})
        
        # Create refresh token
        refresh_token = create_refresh_token({"sub": str(user.id)})
        
        # Save refresh token to database
        # expires_at = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        UserRepository.save_refresh_token(db, user.id, refresh_token, expires_at)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer"
        )