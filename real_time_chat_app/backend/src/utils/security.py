from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from src.config import get_settings

settings = get_settings()

# Password hashing context
pwd_context = CryptContext(schemes=['bcrypt'], deprecated = "auto")


def hash_password(password : str) -> str:
    """
    Hash a plain password using bcrypt.
    
    Time Complexity: O(n) where n is password length + bcrypt rounds
    Space Complexity: O(1)
    
    Args:
        password: Plain text password
        
    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)

def verify_password(plain_password : str, hash_password : str) -> bool:
    """
    Verify a plain password against hashed password.
    
    Time Complexity: O(n) where n is password length + bcrypt rounds
    Space Complexity: O(1)
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Stored hashed password
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hash_password)


def create_access_token(data : dict, expires_delta : Optional[timedelta] = None) -> str:
    """
    Create JWT access token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        data: Dictionary containing user data (e.g., {"sub": "user_id"})
        expires_delta: Optional expiration time override
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({
        "exp": expire,
        "type": "access"
    })

    encoded_jwt =jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def create_refresh_token(data : dict, expires_delta : Optional[timedelta] = None) -> str:
    """
    Create JWT refresh token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        data: Dictionary containing user data
        expires_delta: Optional expiration time override
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta

    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode.update({
        "exp": expire,
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

    return encoded_jwt


def verify_token(token : str, token_type : str = "access") -> Optional[dict]:
    """
    Verify and decode JWT token.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        token: JWT token string
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Decoded token payload if valid, None otherwise
    """

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])

        # Verify token type
        if payload.get("type") != token_type:
            return None
        
        return payload
    
    except JWTError as e:
        print(f"Error {e}")
        return None

