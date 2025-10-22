from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from src.database import get_db
from src.schemas.auth import (
    UserRegister, 
    UserLogin, 
    TokenResponse, 
    TokenRefresh,
    ChangePassword
)
from src.schemas.user import UserResponse
from src.services.auth_service import AuthService
from src.dependencies import get_current_active_user
from src.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=dict, status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user.
    
    Time Complexity: O(1) for database + O(n) for password hashing
    Space Complexity: O(1)
    
    Args:
        user_data: User registration data
        db: Database session
        
    Returns:
        User info and authentication tokens
        
    Raises:
        HTTPException: If username or email already exists
    """
    try:
        user, tokens = AuthService.register_user(db, user_data)
        
        return {
            "message": "User registered successfully",
            "user": user,
            "tokens": tokens
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=dict)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login user and return tokens.
    
    Time Complexity: O(1) for database + O(n) for password verification
    Space Complexity: O(1)
    
    Args:
        login_data: Login credentials
        db: Database session
        
    Returns:
        User info and authentication tokens
        
    Raises:
        HTTPException: If credentials are invalid
    """
    try:
        user, tokens = AuthService.login_user(db, login_data)
        
        return {
            "message": "Login successful",
            "user": user,
            "tokens": tokens
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"}
        )


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        token_data: Refresh token
        db: Database session
        
    Returns:
        New access token
        
    Raises:
        HTTPException: If refresh token is invalid or expired
    """
    try:
        tokens = AuthService.refresh_access_token(db, token_data.refresh_token)
        return tokens
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )


@router.post("/logout", response_model=dict)
def logout(
    token_data: TokenRefresh,
    db: Session = Depends(get_db)
):
    """
    Logout user by deleting refresh token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        token_data: Refresh token to invalidate
        db: Database session
        
    Returns:
        Success message
    """
    success = AuthService.logout_user(db, token_data.refresh_token)
    
    if success:
        return {"message": "Logout successful"}
    
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid refresh token"
    )


@router.post("/logout-all", response_model=dict)
def logout_all_devices(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Logout user from all devices.
    
    Time Complexity: O(n) where n is number of user's sessions
    Space Complexity: O(1)
    
    Args:
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Success message with number of sessions terminated
    """
    count = AuthService.logout_all_devices(db, current_user.id)
    
    return {
        "message": "Logged out from all devices",
        "sessions_terminated": count
    }


@router.post("/change-password", response_model=dict)
def change_password(
    password_data: ChangePassword,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Change user password.
    
    Time Complexity: O(1) + O(n) for password hashing
    Space Complexity: O(1)
    
    Args:
        password_data: Old and new passwords
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Success message
        
    Raises:
        HTTPException: If old password is incorrect
    """
    try:
        AuthService.change_password(
            db, 
            current_user.id, 
            password_data.old_password, 
            password_data.new_password
        )
        
        return {"message": "Password changed successfully. Please login again."}
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/me", response_model=UserResponse)
def get_current_user_info(
    current_user: User = Depends(get_current_active_user)
):
    """
    Get current user information (check session).
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        current_user: Currently authenticated user
        
    Returns:
        Current user information
    """
    return current_user