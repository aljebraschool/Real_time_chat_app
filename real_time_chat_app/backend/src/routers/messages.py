from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.message import MessageCreate, MessageWithSender
from src.schemas.chat import DirectChatResponse
from src.services.chat_service import ChatService
from src.dependencies import get_current_active_user
from src.models.user import User

router = APIRouter(prefix="/messages", tags=["Messages"])


@router.post("/send", response_model=dict, status_code=status.HTTP_201_CREATED)
def send_message(
    message_data: MessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a direct message to another user.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    
    Args:
        message_data: Message data with recipient_id and content
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        Success message with created message data
        
    Raises:
        HTTPException: If recipient not found or validation fails
    """
    try:
        message = ChatService.send_direct_message(db, current_user.id, message_data)
        
        return {
            "message": "Message sent successfully",
            "data": message
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/chat/{other_user_id}", response_model=List[MessageWithSender])
def get_chat_history(
    other_user_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get chat history with another user.
    
    Time Complexity: O(n) where n = limit
    Space Complexity: O(n)
    
    Args:
        other_user_id: ID of the other user
        limit: Maximum number of messages (1-100)
        offset: Number of messages to skip for pagination
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        List of messages with sender information
        
    Raises:
        HTTPException: If other user not found
    """
    try:
        messages = ChatService.get_chat_history(
            db, 
            current_user.id, 
            other_user_id, 
            limit, 
            offset
        )
        return messages
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.get("/chats", response_model=List[DirectChatResponse])
def get_all_chats(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all direct chats for current user.
    
    Time Complexity: O(n) where n = number of user's chats
    Space Complexity: O(n)
    
    Args:
        current_user: Currently authenticated user
        db: Database session
        
    Returns:
        List of direct chats with last message and unread count
    """
    chats = ChatService.get_user_chats(db, current_user.id)
    return chats