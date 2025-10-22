from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, desc
from typing import List, Optional, Tuple
from src.models.chat_room import ChatRoom, RoomType
from src.models.chat_room_member import ChatRoomMember
from src.models.message import Message
from src.models.user import User
from sqlalchemy import func


class ChatRepository:
    """
    Repository for chat-related database operations.
    """
    
    # @staticmethod
    # def get_or_create_direct_chat(db: Session, user1_id: int, user2_id: int) -> ChatRoom:
    #     """
    #     Get existing direct chat between two users or create new one.
        
    #     Time Complexity: O(1) with proper indexing
    #     Space Complexity: O(1)
        
    #     Args:
    #         db: Database session
    #         user1_id: First user ID
    #         user2_id: Second user ID
            
    #     Returns:
    #         ChatRoom object
    #     """
    #     # Find existing direct chat between these two users
    #     existing_chat = db.query(ChatRoom).join(
    #         ChatRoomMember, ChatRoom.id == ChatRoomMember.chat_room_id
    #     ).filter(
    #         ChatRoom.room_type == RoomType.DIRECT,
    #         ChatRoomMember.user_id.in_([user1_id, user2_id])
    #     ).group_by(ChatRoom.id).having(
    #         # db.func.count(ChatRoomMember.user_id) == 2
    #         func.count(ChatRoomMember.user_id) == 2
    #     ).first()
        
    #     if existing_chat:
    #         # Verify both users are members
    #         members = db.query(ChatRoomMember).filter(
    #             ChatRoomMember.chat_room_id == existing_chat.id
    #         ).all()
    #         member_ids = {m.user_id for m in members}
            
    #         if user1_id in member_ids and user2_id in member_ids:
    #             return existing_chat
        
    #     # Create new direct chat
    #     chat_room = ChatRoom(
    #         room_type=RoomType.DIRECT,
    #         created_by=user1_id
    #     )
        
    #     db.add(chat_room)
    #     db.flush()  # Get the chat_room.id without committing
        
    #     # Add both users as members
    #     member1 = ChatRoomMember(chat_room_id=chat_room.id, user_id=user1_id)
    #     member2 = ChatRoomMember(chat_room_id=chat_room.id, user_id=user2_id)
        
    #     db.add(member1)
    #     db.add(member2)
    #     db.commit()
    #     db.refresh(chat_room)
        
    #     return chat_room

    @staticmethod
    def get_or_create_direct_chat(db: Session, user1_id: int, user2_id: int) -> ChatRoom:
        """
        Get existing direct chat between two users or create new one.
        """
        # Always check first (most important!)
        existing = ChatRepository._find_existing_direct_chat(db, user1_id, user2_id)
        if existing:
            return existing
        
        # Create new chat
        try:
            chat_room = ChatRoom(
                room_type=RoomType.DIRECT,
                created_by=user1_id
            )
            db.add(chat_room)
            db.flush()
            
            # Add both users
            member1 = ChatRoomMember(chat_room_id=chat_room.id, user_id=user1_id)
            member2 = ChatRoomMember(chat_room_id=chat_room.id, user_id=user2_id)
            
            db.add(member1)
            db.add(member2)
            db.commit()
            db.refresh(chat_room)
            
            return chat_room
            
        except Exception:
            # Rollback and try to find again
            db.rollback()
            existing = ChatRepository._find_existing_direct_chat(db, user1_id, user2_id)
            if existing:
                return existing
            raise
    
    
    @staticmethod
    def _find_existing_direct_chat(db: Session, user1_id: int, user2_id: int) -> Optional[ChatRoom]:
        """
        Find existing direct chat between two users.
        """
        # Get rooms where user1 is a member
        subquery = db.query(ChatRoomMember.chat_room_id).filter(
            ChatRoomMember.user_id == user1_id
        ).subquery()
        
        # Find direct chat where user2 is also a member
        chat_room = db.query(ChatRoom).filter(
            ChatRoom.room_type == RoomType.DIRECT,
            ChatRoom.id.in_(subquery)
        ).join(ChatRoomMember).filter(
            ChatRoomMember.user_id == user2_id
        ).first()
        
        return chat_room
    
    
    @staticmethod
    def create_message(db: Session, chat_room_id: int, sender_id: int, content: str) -> Message:
        """
        Create a new message.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            sender_id: Sender user ID
            content: Message content
            
        Returns:
            Created Message object
        """
        message = Message(
            chat_room_id=chat_room_id,
            sender_id=sender_id,
            content=content
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        return message
    
    
    @staticmethod
    def get_chat_messages(db: Session, chat_room_id: int, limit: int = 50, 
                         offset: int = 0) -> List[Message]:
        """
        Get messages from a chat room (paginated).
        
        Time Complexity: O(n) where n = limit
        Space Complexity: O(n)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            limit: Maximum number of messages to return
            offset: Number of messages to skip
            
        Returns:
            List of Message objects (newest first)
        """
        messages = db.query(Message).filter(
            Message.chat_room_id == chat_room_id
        ).order_by(desc(Message.created_at)).limit(limit).offset(offset).all()
        
        return list(reversed(messages))  # Return oldest to newest
    
    
    @staticmethod
    def get_user_chat_rooms(db: Session, user_id: int) -> List[Tuple[ChatRoom, User, Message]]:
        """
        Get all chat rooms for a user with last message and other user info.
        
        Time Complexity: O(n) where n = number of user's chats
        Space Complexity: O(n)
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            List of tuples (ChatRoom, OtherUser, LastMessage)
        """
        # Get user's chat room IDs
        chat_room_ids = db.query(ChatRoomMember.chat_room_id).filter(
            ChatRoomMember.user_id == user_id
        ).all()
        
        chat_room_ids = [cid[0] for cid in chat_room_ids]
        
        results = []
        
        for room_id in chat_room_ids:
            # Get chat room
            chat_room = db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
            
            if not chat_room:
                continue
            
            # Get other user (for direct chats)
            other_user = None
            if chat_room.room_type == RoomType.DIRECT:
                other_user_id = db.query(ChatRoomMember.user_id).filter(
                    and_(
                        ChatRoomMember.chat_room_id == room_id,
                        ChatRoomMember.user_id != user_id
                    )
                ).first()
                
                if other_user_id:
                    other_user = db.query(User).filter(User.id == other_user_id[0]).first()
            
            # Get last message
            last_message = db.query(Message).filter(
                Message.chat_room_id == room_id
            ).order_by(desc(Message.created_at)).first()
            
            results.append((chat_room, other_user, last_message))
        
        return results
    
    
    @staticmethod
    def is_user_in_chat(db: Session, user_id: int, chat_room_id: int) -> bool:
        """
        Check if user is a member of chat room.
        
        Time Complexity: O(1) with proper indexing
        Space Complexity: O(1)
        
        Args:
            db: Database session
            user_id: User ID
            chat_room_id: Chat room ID
            
        Returns:
            True if user is member, False otherwise
        """
        member = db.query(ChatRoomMember).filter(
            and_(
                ChatRoomMember.user_id == user_id,
                ChatRoomMember.chat_room_id == chat_room_id
            )
        ).first()
        
        return member is not None
    
    
    @staticmethod
    def mark_messages_as_read(db: Session, chat_room_id: int, user_id: int) -> int:
        """
        Mark all messages in chat room as read for user.
        
        Time Complexity: O(n) where n = unread messages
        Space Complexity: O(1)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            user_id: User ID (messages sent by this user won't be marked)
            
        Returns:
            Number of messages marked as read
        """
        count = db.query(Message).filter(
            and_(
                Message.chat_room_id == chat_room_id,
                Message.sender_id != user_id,
                Message.is_read == False
            )
        ).update({"is_read": True})
        
        db.commit()
        return count


    @staticmethod
    def create_group_chat(db: Session, name: str, creator_id: int, member_ids: List[int]) -> ChatRoom:
        """
        Create a new group chat.
        
        Time Complexity: O(n) where n = number of members
        Space Complexity: O(n)
        
        Args:
            db: Database session
            name: Group name
            creator_id: Creator user ID
            member_ids: List of user IDs to add (including creator)
            
        Returns:
            Created ChatRoom object
        """
        # Create group chat room
        chat_room = ChatRoom(
            name=name,
            room_type=RoomType.GROUP,
            created_by=creator_id
        )
        db.add(chat_room)
        db.flush()
        
        # Add creator if not in member_ids
        if creator_id not in member_ids:
            member_ids.append(creator_id)
        
        # Add all members
        for user_id in member_ids:
            member = ChatRoomMember(chat_room_id=chat_room.id, user_id=user_id)
            db.add(member)
        
        db.commit()
        db.refresh(chat_room)
        return chat_room
    
    
    @staticmethod
    def add_group_members(db: Session, chat_room_id: int, user_ids: List[int]) -> int:
        """
        Add members to a group chat.
        
        Time Complexity: O(n) where n = number of users to add
        Space Complexity: O(1)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            user_ids: List of user IDs to add
            
        Returns:
            Number of members added
        """
        added = 0
        for user_id in user_ids:
            # Check if already a member
            existing = db.query(ChatRoomMember).filter(
                and_(
                    ChatRoomMember.chat_room_id == chat_room_id,
                    ChatRoomMember.user_id == user_id
                )
            ).first()
            
            if not existing:
                member = ChatRoomMember(chat_room_id=chat_room_id, user_id=user_id)
                db.add(member)
                added += 1
        
        db.commit()
        return added
    
    
    @staticmethod
    def remove_group_member(db: Session, chat_room_id: int, user_id: int) -> bool:
        """
        Remove a member from group chat.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            user_id: User ID to remove
            
        Returns:
            True if removed, False if not found
        """
        member = db.query(ChatRoomMember).filter(
            and_(
                ChatRoomMember.chat_room_id == chat_room_id,
                ChatRoomMember.user_id == user_id
            )
        ).first()
        
        if member:
            db.delete(member)
            db.commit()
            return True
        
        return False
    
    
    @staticmethod
    def get_group_members(db: Session, chat_room_id: int) -> List[User]:
        """
        Get all members of a group chat.
        
        Time Complexity: O(n) where n = number of members
        Space Complexity: O(n)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            
        Returns:
            List of User objects
        """
        members = db.query(User).join(
            ChatRoomMember, User.id == ChatRoomMember.user_id
        ).filter(
            ChatRoomMember.chat_room_id == chat_room_id
        ).all()
        
        return members
    
    
    @staticmethod
    def get_chat_room_by_id(db: Session, chat_room_id: int) -> Optional[ChatRoom]:
        """
        Get chat room by ID.
        
        Time Complexity: O(1)
        Space Complexity: O(1)
        
        Args:
            db: Database session
            chat_room_id: Chat room ID
            
        Returns:
            ChatRoom object or None
        """
        return db.query(ChatRoom).filter(ChatRoom.id == chat_room_id).first()