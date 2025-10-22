from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.schemas.chat import (
    GroupCreate, 
    GroupMemberAdd, 
    GroupMemberRemove,
    GroupMessageCreate
)
from src.schemas.message import MessageWithSender
from src.services.chat_service import ChatService
from src.dependencies import get_current_active_user
from src.models.user import User

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/create", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_group(
    group_data: GroupCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Create a new group chat.
    
    Time Complexity: O(n) where n = number of members
    Space Complexity: O(n)
    """
    try:
        group = ChatService.create_group(
            db, 
            current_user.id, 
            group_data.name, 
            group_data.member_ids
        )
        
        return {
            "message": "Group created successfully",
            "group": group
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/send", response_model=dict, status_code=status.HTTP_201_CREATED)
def send_group_message(
    message_data: GroupMessageCreate,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Send a message to a group.
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    try:
        message = ChatService.send_group_message(
            db, 
            current_user.id, 
            message_data.group_id, 
            message_data.content
        )
        
        return {
            "message": "Message sent successfully",
            "data": message
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{group_id}/messages", response_model=List[MessageWithSender])
def get_group_messages(
    group_id: int,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get messages from a group.
    
    Time Complexity: O(n) where n = limit
    Space Complexity: O(n)
    """
    try:
        messages = ChatService.get_group_messages(
            db, 
            current_user.id, 
            group_id, 
            limit, 
            offset
        )
        return messages
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.post("/{group_id}/members", response_model=dict)
def add_group_members(
    group_id: int,
    member_data: GroupMemberAdd,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Add members to a group (creator only).
    
    Time Complexity: O(n) where n = number of members to add
    Space Complexity: O(1)
    """
    try:
        added = ChatService.add_members_to_group(
            db, 
            current_user.id, 
            group_id, 
            member_data.user_ids
        )
        
        return {
            "message": f"Successfully added {added} members",
            "members_added": added
        }
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.delete("/{group_id}/members", response_model=dict)
def remove_group_member(
    group_id: int,
    member_data: GroupMemberRemove,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Remove a member from group (creator only or leave group).
    
    Time Complexity: O(1)
    Space Complexity: O(1)
    """
    try:
        ChatService.remove_member_from_group(
            db, 
            current_user.id, 
            group_id, 
            member_data.user_id
        )
        
        return {"message": "Member removed successfully"}
    
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e)
        )


@router.get("/my-groups", response_model=List[dict])
def get_my_groups(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get all groups user is member of.
    
    Time Complexity: O(n) where n = number of user's groups
    Space Complexity: O(n)
    """
    groups = ChatService.get_user_groups(db, current_user.id)
    return groups