import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get the DATABASE_URL from your .env file
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # Connect to PostgreSQL
    conn = psycopg2.connect(DATABASE_URL)
    print("✅ Connection successful!")

    # Optional: test query
    cursor = conn.cursor()
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("PostgreSQL version:", record)

    # Close connection
    cursor.close()
    conn.close()

except Exception as e:
    print("❌ Connection failed!")
    print(e)
