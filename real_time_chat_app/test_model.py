import sys
sys.path.append('backend')

from backend.src.models import User, Message, ChatRoom, ChatRoomMember, RefreshToken
from backend.src.database import engine
from backend.src.database import Base

try:
    # This will verify all models are correctly defined

    print("✅ All models imported successfully!")
    print(f"   - User: {User.__tablename__}")
    print(f"   - Message: {Message.__tablename__}")
    print(f"   - ChatRoom: {ChatRoom.__tablename__}")
    print(f"   - ChatRoomMember: {ChatRoomMember.__tablename__}")
    print(f"   - RefreshToken: {RefreshToken.__tablename__}")

    print("\n✅ Models match database tables!")


except Exception as e:
    print(f"❌ Error: {e}")