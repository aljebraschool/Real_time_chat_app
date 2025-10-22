from sqlalchemy.orm import Session
from typing import List, Optional
from src.repositories.chat_repository import ChatRepository
from src.repositories.user_repository import UserRepository
from src.schemas.message import MessageCreate, MessageResponse, MessageWithSender
from src.schemas.chat import DirectChatResponse
from src.models.user import User
from src.models.message import Message
from sqlalchemy import and_


class ChatService:
    """
    Chat service containing business logic for messaging.
    """
    
    @staticmethod
    def send_direct_message(db: Session, sender_id: int, message_data: MessageCreate) -> MessageResponse:
        """
        Send a direct message to another user.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            sender_id: Sender user ID
            message_data: Message data with recipient_id and content
            
        Returns:
            Created message
            
        Raises:
            ValueError: If recipient doesn't exist or is same as sender
        """
        # Validate recipient exists
        recipient = UserRepository.get_user_by_id(db, message_data.recipient_id)
        if not recipient:
            raise ValueError("Recipient user not found")
        
        # Can't send message to yourself
        if sender_id == message_data.recipient_id:
            raise ValueError("Cannot send message to yourself")
        
        # Get or create direct chat room
        chat_room = ChatRepository.get_or_create_direct_chat(db, sender_id, message_data.recipient_id)
        
        # Create message
        message = ChatRepository.create_message(
            db=db,
            chat_room_id=chat_room.id,
            sender_id=sender_id,
            content=message_data.content
        )
        
        return MessageResponse.model_validate(message)
    
    
    @staticmethod
    def get_chat_history(db: Session, user_id: int, other_user_id: int, 
                        limit: int = 50, offset: int = 0) -> List[MessageWithSender]:
        """
        Get chat history between two users.
        
        Time Complexity: O(n) where n = limit
        Space Complexity: O(n)
        
        Args:
            db: Database session
            user_id: Current user ID
            other_user_id: Other user ID
            limit: Maximum messages to return
            offset: Number of messages to skip
            
        Returns:
            List of messages with sender info
            
        Raises:
            ValueError: If other user doesn't exist
        """
        # Validate other user exists
        other_user = UserRepository.get_user_by_id(db, other_user_id)
        if not other_user:
            raise ValueError("User not found")
        
        # Get or create chat room
        chat_room = ChatRepository.get_or_create_direct_chat(db, user_id, other_user_id)
        
        # Get messages
        messages = ChatRepository.get_chat_messages(db, chat_room.id, limit, offset)
        
        # Mark messages as read
        ChatRepository.mark_messages_as_read(db, chat_room.id, user_id)
        
        # Convert to response with sender info
        result = []
        for msg in messages:
            sender = UserRepository.get_user_by_id(db, msg.sender_id) if msg.sender_id else None
            
            msg_with_sender = MessageWithSender(
                id=msg.id,
                chat_room_id=msg.chat_room_id,
                sender_id=msg.sender_id,
                content=msg.content,
                is_read=msg.is_read,
                created_at=msg.created_at,
                sender_username=sender.username if sender else None,
                sender_full_name=sender.full_name if sender else None
            )
            result.append(msg_with_sender)
        
        return result
    
    
    # @staticmethod
    # def get_user_chats(db: Session, user_id: int) -> List[DirectChatResponse]:
    #     """
    #     Get all direct chats for a user.
        
    #     Time Complexity: O(n) where n = number of user's chats
    #     Space Complexity: O(n)
        
    #     Args:
    #         db: Database session
    #         user_id: User ID
            
    #     Returns:
    #         List of direct chats with other user info and last message
    #     """
    #     chat_data = ChatRepository.get_user_chat_rooms(db, user_id)
        
    #     result = []
        
    #     for chat_room, other_user, last_message in chat_data:
    #         # Skip if no other user (shouldn't happen for direct chats)
    #         if not other_user:
    #             continue
            
    #         # Count unread messages
    #         unread_count = db.query(db.func.count()).select_from(
    #             db.query(db.models.Message).filter(
    #                 db.and_(
    #                     db.models.Message.chat_room_id == chat_room.id,
    #                     db.models.Message.sender_id != user_id,
    #                     db.models.Message.is_read == False
    #                 )
    #             ).subquery()
    #         ).scalar() or 0
            
    #         chat_response = DirectChatResponse(
    #             chat_room_id=chat_room.id,
    #             other_user_id=other_user.id,
    #             other_user_username=other_user.username,
    #             other_user_full_name=other_user.full_name,
    #             last_message=last_message.content if last_message else None,
    #             last_message_time=last_message.created_at if last_message else None,
    #             unread_count=unread_count
    #         )
    #         result.append(chat_response)
        
    #     # Sort by last message time (newest first)
    #     result.sort(key=lambda x: x.last_message_time or chat_room.created_at, reverse=True)
        
    #     return result

    # @staticmethod
    # def get_user_chats(db: Session, user_id: int) -> List[DirectChatResponse]:
    #     """
    #     Get all direct chats for a user.
        
    #     Time Complexity: O(n) where n = number of user's chats
    #     Space Complexity: O(n)
        
    #     Args:
    #         db: Database session
    #         user_id: User ID
            
    #     Returns:
    #         List of direct chats with other user info and last message
    #     """
    #     from src.models.message import Message
    #     from sqlalchemy import and_
        
    #     chat_data = ChatRepository.get_user_chat_rooms(db, user_id)
        
    #     result = []
        
    #     for chat_room, other_user, last_message in chat_data:
    #         # Skip if no other user (shouldn't happen for direct chats)
    #         if not other_user:
    #             continue
            
    #         # Count unread messages
    #         unread_count = db.query(Message).filter(
    #             and_(
    #                 Message.chat_room_id == chat_room.id,
    #                 Message.sender_id != user_id,
    #                 Message.is_read == False
    #             )
    #         ).count()
            
    #         chat_response = DirectChatResponse(
    #             chat_room_id=chat_room.id,
    #             other_user_id=other_user.id,
    #             other_user_username=other_user.username,
    #             other_user_full_name=other_user.full_name,
    #             last_message=last_message.content if last_message else None,
    #             last_message_time=last_message.created_at if last_message else None,
    #             unread_count=unread_count
    #         )
    #         result.append(chat_response)
        
    #     # Sort by last message time (newest first)
    #     result.sort(key=lambda x: x.last_message_time or chat_room.created_at, reverse=True)
        
    #     return result

    @staticmethod
    def get_user_chats(db: Session, user_id: int) -> List[DirectChatResponse]:
        """
        Get all direct chats for a user.
        """
        
        
        chat_data = ChatRepository.get_user_chat_rooms(db, user_id)
        
        result = []
        
        for item in chat_data:
            # Safely unpack tuple
            if not item or len(item) < 3:
                continue
            
            chat_room = item[0]
            other_user = item[1]
            last_message = item[2]
            
            # Skip if no chat room or not a direct chat
            if not chat_room or chat_room.room_type != "direct":
                continue
            
            # Skip if no other user (shouldn't happen for direct chats)
            if not other_user:
                continue
            
            # Count unread messages
            unread_count = db.query(Message).filter(
                and_(
                    Message.chat_room_id == chat_room.id,
                    Message.sender_id != user_id,
                    Message.is_read == False
                )
            ).count()
            
            chat_response = DirectChatResponse(
                chat_room_id=chat_room.id,
                other_user_id=other_user.id,
                other_user_username=other_user.username,
                other_user_full_name=other_user.full_name,
                last_message=last_message.content if last_message else None,
                last_message_time=last_message.created_at if last_message else None,
                unread_count=unread_count
            )
            result.append(chat_response)
        
        # Sort by last message time (newest first)
        result.sort(
            key=lambda x: x.last_message_time if x.last_message_time else chat_room.created_at, 
            reverse=True
        )
        
        return result
    
    
    @staticmethod
    def verify_chat_access(db: Session, user_id: int, chat_room_id: int) -> bool:
        """
        Verify user has access to chat room.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            chat_room_id: Chat room ID
            
        Returns:
            True if user has access, False otherwise
        """
        return ChatRepository.is_user_in_chat(db, user_id, chat_room_id)
    
    @staticmethod
    def create_group(db: Session, creator_id: int, name: str, member_ids: List[int]) -> dict:
        """
        Create a new group chat.
        
        Time Complexity: O(n) where n = number of members
        Space Complexity: O(n)
        
        Args:
            db: Database session
            creator_id: Creator user ID
            name: Group name
            member_ids: List of user IDs to add
            
        Returns:
            Dictionary with group info
            
        Raises:
            ValueError: If validation fails
        """
        # Validate all users exist
        for user_id in member_ids:
            user = UserRepository.get_user_by_id(db, user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} not found")
        
        # Create group
        group = ChatRepository.create_group_chat(db, name, creator_id, member_ids)
        
        # Get member count
        members = ChatRepository.get_group_members(db, group.id)
        
        return {
            "id": group.id,
            "name": group.name,
            "room_type": group.room_type,
            "created_by": group.created_by,
            "member_count": len(members),
            "created_at": group.created_at
        }
    
    
    @staticmethod
    def send_group_message(db: Session, sender_id: int, group_id: int, content: str) -> MessageResponse:
        """
        Send a message to a group chat.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            sender_id: Sender user ID
            group_id: Group chat room ID
            content: Message content
            
        Returns:
            Created message
            
        Raises:
            ValueError: If user not in group or group doesn't exist
        """
        # Verify group exists
        group = ChatRepository.get_chat_room_by_id(db, group_id)
        if not group:
            raise ValueError("Group not found")
        
        if group.room_type != "group":
            raise ValueError("This is not a group chat")
        
        # Verify user is member
        if not ChatRepository.is_user_in_chat(db, sender_id, group_id):
            raise ValueError("You are not a member of this group")
        
        # Create message
        message = ChatRepository.create_message(db, group_id, sender_id, content)
        
        return MessageResponse.model_validate(message)
    
    
    @staticmethod
    def get_group_messages(db: Session, user_id: int, group_id: int, 
                          limit: int = 50, offset: int = 0) -> List[MessageWithSender]:
        """
        Get messages from a group chat.
        
        Time Complexity: O(n) where n = limit
        Space Complexity: O(n)
        
        Args:
            db: Database session
            user_id: Current user ID
            group_id: Group chat room ID
            limit: Maximum messages to return
            offset: Number of messages to skip
            
        Returns:
            List of messages with sender info
            
        Raises:
            ValueError: If user not in group
        """
        # Verify user is member
        if not ChatRepository.is_user_in_chat(db, user_id, group_id):
            raise ValueError("You are not a member of this group")
        
        # Get messages
        messages = ChatRepository.get_chat_messages(db, group_id, limit, offset)
        
        # Convert to response with sender info
        result = []
        for msg in messages:
            sender = UserRepository.get_user_by_id(db, msg.sender_id) if msg.sender_id else None
            
            msg_with_sender = MessageWithSender(
                id=msg.id,
                chat_room_id=msg.chat_room_id,
                sender_id=msg.sender_id,
                content=msg.content,
                is_read=msg.is_read,
                created_at=msg.created_at,
                sender_username=sender.username if sender else None,
                sender_full_name=sender.full_name if sender else None
            )
            result.append(msg_with_sender)
        
        return result
    
    
    @staticmethod
    def add_members_to_group(db: Session, user_id: int, group_id: int, user_ids: List[int]) -> int:
        """
        Add members to a group (only creator can add).
        
        Time Complexity: O(n) where n = number of users to add
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: Current user ID (must be creator)
            group_id: Group chat room ID
            user_ids: List of user IDs to add
            
        Returns:
            Number of members added
            
        Raises:
            ValueError: If not creator or group doesn't exist
        """
        # Get group
        group = ChatRepository.get_chat_room_by_id(db, group_id)
        if not group:
            raise ValueError("Group not found")
        
        # Verify user is creator
        if group.created_by != user_id:
            raise ValueError("Only group creator can add members")
        
        # Validate all users exist
        for uid in user_ids:
            user = UserRepository.get_user_by_id(db, uid)
            if not user:
                raise ValueError(f"User with ID {uid} not found")
        
        # Add members
        added = ChatRepository.add_group_members(db, group_id, user_ids)
        
        return added
    
    
    @staticmethod
    def remove_member_from_group(db: Session, user_id: int, group_id: int, member_id: int) -> bool:
        """
        Remove a member from group (creator only, or user can leave).
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: Current user ID
            group_id: Group chat room ID
            member_id: User ID to remove
            
        Returns:
            True if removed
            
        Raises:
            ValueError: If not authorized or group doesn't exist
        """
        # Get group
        group = ChatRepository.get_chat_room_by_id(db, group_id)
        if not group:
            raise ValueError("Group not found")
        
        # Check authorization (creator can remove anyone, user can remove self)
        if group.created_by != user_id and member_id != user_id:
            raise ValueError("Not authorized to remove this member")
        
        # Remove member
        removed = ChatRepository.remove_group_member(db, group_id, member_id)
        
        if not removed:
            raise ValueError("Member not found in group")
        
        return True
    
    
    @staticmethod
    def get_user_groups(db: Session, user_id: int) -> List[dict]:
        """
        Get all groups user is member of.
        
        Time Complexity: O(n) where n = number of user's groups
        Space Complexity: O(n)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of group info dictionaries
        """
        chat_data = ChatRepository.get_user_chat_rooms(db, user_id)
        
        result = []
        
        for chat_room, _, last_message in chat_data:
            # Only include group chats
            if chat_room.room_type != "group":
                continue
            
            # Get member count
            members = ChatRepository.get_group_members(db, chat_room.id)
            
            group_info = {
                "id": chat_room.id,
                "name": chat_room.name,
                "room_type": chat_room.room_type,
                "created_by": chat_room.created_by,
                "member_count": len(members),
                "last_message": last_message.content if last_message else None,
                "last_message_time": last_message.created_at if last_message else None,
                "created_at": chat_room.created_at
            }
            result.append(group_info)
        
        return result