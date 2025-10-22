from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from typing import Optional
from src.database import get_db
from src.services.auth_service import AuthService
from src.models.user import User

# HTTP Bearer token scheme
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Usage:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user": current_user.username}
    
    Args:
        credentials: Bearer token from Authorization header
        db: Database session
        
    Returns:
        Current User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    user = AuthService.get_current_user(db, token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Dependency to ensure user is active.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Usage:
        @app.get("/protected")
        def protected_route(user: User = Depends(get_current_active_user)):
            return {"user": user.username}
    
    Args:
        current_user: Current user from get_current_user dependency
        
    Returns:
        Active User object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return current_user


def get_optional_current_user(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False)),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency to get current user if token is provided (optional authentication).
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Usage:
        @app.get("/public-or-protected")
        def route(user: Optional[User] = Depends(get_optional_current_user)):
            if user:
                return {"message": f"Hello {user.username}"}
            return {"message": "Hello guest"}
    
    Args:
        credentials: Optional bearer token
        db: Database session
        
    Returns:
        User object if authenticated, None otherwise
    """
    if not credentials:
        return None
    
    token = credentials.credentials
    return AuthService.get_current_user(db, token)