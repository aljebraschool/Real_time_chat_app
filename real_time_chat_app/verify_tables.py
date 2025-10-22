from backend.src.database import engine
from sqlalchemy import text

try:
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        
        tables = [row[0] for row in result]
        
        if tables:
            print("✅ Tables found:")
            for table in tables:
                print(f"   - {table}")
        else:
            print("⚠️ No tables found. Run init_schema.sql in pgAdmin")
            
except Exception as e:
    print(f"❌ Error: {e}")

