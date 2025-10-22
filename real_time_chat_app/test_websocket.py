import asyncio
import websockets
import json


async def test_websocket():
    """
    Test WebSocket connection and messaging.
    Replace YOUR_ACCESS_TOKEN with a real token from login.
    """
    
    # Get token first (login via API)
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyIiwiZXhwIjoxNzYwOTk2MzM3LCJ0eXBlIjoiYWNjZXNzIn0.LAu0iUg3kIABlCkG5z40YX5gXH3kHUHj5oAm0yh5Ysg"  # Replace this!
    
    uri = f"ws://127.0.0.1:8000/ws/{token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            print("✅ Connected to WebSocket")
            
            # Receive connection confirmation
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            # Join a room (use real room_id from your database)
            join_message = {
                "type": "join_room",
                "room_id": 1  # Change to your room ID
            }
            await websocket.send(json.dumps(join_message))
            print(f"📤 Sent: {join_message}")
            
            # Receive join confirmation
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            # Send a message
            message = {
                "type": "message",
                "room_id": 9,  # Change to your room ID
                "content": "Hello from WebSocket test!"
            }
            await websocket.send(json.dumps(message))
            print(f"📤 Sent: {message}")
            
            # Receive broadcast
            response = await websocket.recv()
            print(f"📨 Received: {response}")
            
            # Send typing indicator
            typing = {
                "type": "typing",
                "room_id": 9
            }
            await websocket.send(json.dumps(typing))
            print(f"📤 Sent: {typing}")
            
            # Keep connection open for a bit
            print("\n⏳ Keeping connection open for 5 seconds...")
            await asyncio.sleep(5)
            
            print("✅ Test completed successfully!")
    
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    print("🚀 WebSocket Test Client")
    print("=" * 50)
    print("\n⚠️  IMPORTANT: Replace YOUR_ACCESS_TOKEN_HERE with a real token!")
    print("   1. Start server: uvicorn src.main:app --reload")
    print("   2. Login via /docs to get token")
    print("   3. Replace token in this file")
    print("   4. Run: python test_websocket.py\n")
    
    asyncio.run(test_websocket())