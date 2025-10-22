# 💬 Real-Time Chat Application

A production-ready, full-stack real-time chat application built with **FastAPI**, **PostgreSQL**, **WebSockets**, and **Streamlit**. Features secure authentication, one-to-one messaging, group chats, and real-time communication.

---

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [WebSocket Usage](#websocket-usage)
- [Testing](#testing)
- [Database Schema](#database-schema)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)

---

## ✨ Features

### Authentication
- ✅ User registration with validation
- ✅ Secure login with JWT tokens
- ✅ Access & refresh token mechanism
- ✅ Password hashing with bcrypt
- ✅ Session management
- ✅ Password change functionality
- ✅ Logout from single/all devices

### Messaging
- ✅ **One-to-One Chat**: Direct messaging between users
- ✅ **Group Chat**: Create and manage group conversations
- ✅ **Real-time Communication**: Instant message delivery via WebSockets
- ✅ **Message History**: Paginated chat history retrieval
- ✅ **Typing Indicators**: See when someone is typing
- ✅ **Online Status**: Track who's currently online
- ✅ **Unread Message Count**: Know how many unread messages you have

### Group Management
- ✅ Create groups with multiple members
- ✅ Add/remove members (creator only)
- ✅ Leave groups
- ✅ Group message broadcasting

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern, fast web framework
- **PostgreSQL** - Reliable relational database
- **SQLAlchemy** - SQL toolkit and ORM
- **WebSockets** - Real-time bidirectional communication
- **JWT** - Secure token-based authentication
- **Pydantic** - Data validation
- **Pytest** - Testing framework

### Frontend
- **Streamlit** - Rapid UI development

### Security
- **Bcrypt** - Password hashing
- **python-jose** - JWT token handling
- **Passlib** - Password utilities

---

## 📁 Project Structure
```
real-time-chat-app/
├── backend/
│   ├── src/
│   │   ├── __init__.py
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── config.py                  # Environment configuration
│   │   ├── database.py                # Database connection
│   │   ├── dependencies.py            # Auth dependencies
│   │   │
│   │   ├── db/
│   │   │   └── migrations/
│   │   │       └── init_schema.sql    # Database schema
│   │   │
│   │   ├── models/                    # SQLAlchemy models
│   │   │   ├── user.py
│   │   │   ├── chat_room.py
│   │   │   ├── chat_room_member.py
│   │   │   ├── message.py
│   │   │   └── refresh_token.py
│   │   │
│   │   ├── schemas/                   # Pydantic schemas
│   │   │   ├── auth.py
│   │   │   ├── user.py
│   │   │   ├── message.py
│   │   │   └── chat.py
│   │   │
│   │   ├── repositories/              # Database operations
│   │   │   ├── user_repository.py
│   │   │   └── chat_repository.py
│   │   │
│   │   ├── services/                  # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── chat_service.py
│   │   │   └── websocket_manager.py
│   │   │
│   │   ├── routers/                   # API endpoints
│   │   │   ├── auth.py
│   │   │   ├── messages.py
│   │   │   ├── groups.py
│   │   │   └── websocket.py
│   │   │
│   │   └── utils/                     # Helper functions
│   │       └── security.py
│   │
│   └── tests/                         # Test suite
│       ├── conftest.py
│       ├── test_auth.py
│       ├── test_chat.py
│       └── test_groups.py
│
├── frontend/
│   ├── app.py                         # Main Streamlit app
│   ├── pages/
│   │   ├── 1_🔐_Login.py
│   │   ├── 2_💬_Chat.py
│   │   └── 3_👥_Groups.py
│   └── utils/
│       └── api_client.py              # Backend API client
│
├── .env                               # Environment variables
├── requirements.txt                   # Python dependencies
└── README.md                          # This file
```

---

## 📦 Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **pip** - Python package manager (comes with Python)
- **Git** - [Download](https://git-scm.com/)

Optional:
- **pgAdmin** - PostgreSQL GUI tool
- **Postman** - API testing (or use built-in Swagger docs)

---

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/real-time-chat-app.git
cd real-time-chat-app
```

### 2. Create Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Setup PostgreSQL Database

**Option A: Using pgAdmin**

1. Open pgAdmin
2. Right-click "Databases" → Create → Database
3. Database name: `chatapp`
4. Click "Save"

**Option B: Using Command Line**
```bash
# Login to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE chatapp;

# Exit
\q
```

### 5. Create Database Tables

1. Open pgAdmin
2. Navigate to `chatapp` database
3. Click "Query Tool"
4. Copy and paste the entire content from `backend/src/db/migrations/init_schema.sql`
5. Click "Execute" (▶️ button)

**Verify tables created:**
```sql
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public';
```

You should see: `users`, `chat_rooms`, `chat_room_members`, `messages`, `refresh_tokens`

---

## ⚙️ Configuration

### 1. Create Environment File

Create `.env` file in the project root:
```bash
# Database Configuration
DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/chatapp

# JWT Authentication
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# App Settings
DEBUG=True
APP_NAME=RealtimeChatApp
```

### 2. Generate SECRET_KEY
```bash
# Run this command to generate a secure secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

Copy the output and replace `your-secret-key-here` in `.env`

### 3. Update Database URL

Replace `YOUR_PASSWORD` with your PostgreSQL password in the `DATABASE_URL`.

**Example:**
```
DATABASE_URL=postgresql://postgres:mypassword123@localhost:5432/chatapp
```

---

## 🏃 Running the Application

### Start Backend Server
```bash
cd backend
uvicorn src.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Application startup complete.
```

### Start Frontend (In Another Terminal)
```bash
# Activate virtual environment first
source venv/bin/activate  # or venv\Scripts\activate on Windows

cd frontend
streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Access the Application

- **Frontend UI**: http://localhost:8501
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

---

## 📚 API Documentation

### Interactive API Docs

Visit `http://localhost:8000/docs` for interactive Swagger documentation where you can test all endpoints.

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "securepass123",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "is_active": true
  },
  "tokens": {
    "access_token": "eyJhbGc...",
    "refresh_token": "eyJhbGc...",
    "token_type": "bearer"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "securepass123"
}
```

#### Get Current User
```http
GET /auth/me
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Refresh Token
```http
POST /auth/refresh
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

#### Logout
```http
POST /auth/logout
Content-Type: application/json

{
  "refresh_token": "YOUR_REFRESH_TOKEN"
}
```

### Messaging Endpoints

#### Send Direct Message
```http
POST /messages/send
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "recipient_id": 2,
  "content": "Hello! How are you?"
}
```

#### Get Chat History
```http
GET /messages/chat/{other_user_id}?limit=50&offset=0
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Get All Chats
```http
GET /messages/chats
Authorization: Bearer YOUR_ACCESS_TOKEN
```

### Group Endpoints

#### Create Group
```http
POST /groups/create
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "name": "Team Discussion",
  "member_ids": [2, 3, 4]
}
```

#### Send Group Message
```http
POST /groups/send
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "group_id": 1,
  "content": "Hello team!"
}
```

#### Get Group Messages
```http
GET /groups/{group_id}/messages?limit=50
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Get My Groups
```http
GET /groups/my-groups
Authorization: Bearer YOUR_ACCESS_TOKEN
```

#### Add Members to Group
```http
POST /groups/{group_id}/members
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "user_ids": [5, 6]
}
```

#### Remove Member from Group
```http
DELETE /groups/{group_id}/members
Authorization: Bearer YOUR_ACCESS_TOKEN
Content-Type: application/json

{
  "user_id": 5
}
```

---

## 🔌 WebSocket Usage

### Connect to WebSocket
```javascript
// JavaScript/TypeScript example
const token = "YOUR_ACCESS_TOKEN";
const ws = new WebSocket(`ws://localhost:8000/ws/${token}`);

ws.onopen = () => {
    console.log("Connected to chat server");
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log("Received:", data);
};
```

### WebSocket Message Types

#### 1. Join Room
```json
{
  "type": "join_room",
  "room_id": 1
}
```

#### 2. Send Message
```json
{
  "type": "message",
  "room_id": 1,
  "content": "Hello everyone!"
}
```

#### 3. Leave Room
```json
{
  "type": "leave_room",
  "room_id": 1
}
```

#### 4. Typing Indicator
```json
{
  "type": "typing",
  "room_id": 1
}
```

#### 5. Ping (Keep-Alive)
```json
{
  "type": "ping"
}
```

### Received Message Types

#### Connection Confirmation
```json
{
  "type": "connected",
  "user_id": 1,
  "username": "john_doe",
  "message": "Connected to chat server"
}
```

#### New Message
```json
{
  "type": "new_message",
  "room_id": 1,
  "message_id": 42,
  "sender_id": 2,
  "sender_username": "jane_doe",
  "content": "Hi there!",
  "created_at": "2025-10-20T10:30:00"
}
```

#### User Joined Room
```json
{
  "type": "user_joined",
  "room_id": 1,
  "user_id": 3,
  "username": "bob_smith"
}
```

#### User Left Room
```json
{
  "type": "user_left",
  "room_id": 1,
  "user_id": 3,
  "username": "bob_smith"
}
```

#### User Typing
```json
{
  "type": "user_typing",
  "room_id": 1,
  "user_id": 2,
  "username": "jane_doe"
}
```

---

## 🧪 Testing

### Setup Test Database

Create a separate test database:
```bash
# Login to PostgreSQL
psql -U postgres

# Create test database
CREATE DATABASE chatapp_test;

# Exit
\q
```

### Run All Tests
```bash
cd backend
pytest tests/ -v
```

### Run Specific Test File
```bash
# Test authentication
pytest tests/test_auth.py -v

# Test messaging
pytest tests/test_chat.py -v

# Test groups
pytest tests/test_groups.py -v
```

### Run Single Test
```bash
pytest tests/test_auth.py::test_register_user -v
```

### Test Coverage
```bash
pytest --cov=src tests/
```

---

## 🗄️ Database Schema

### Tables Overview

#### users
Stores user account information.

| Column          | Type         | Description                |
|-----------------|--------------|----------------------------|
| id              | SERIAL       | Primary key                |
| username        | VARCHAR(50)  | Unique username            |
| email           | VARCHAR(100) | Unique email               |
| hashed_password | VARCHAR(255) | Bcrypt hashed password     |
| full_name       | VARCHAR(100) | User's full name           |
| is_active       | BOOLEAN      | Account status             |
| is_verified     | BOOLEAN      | Email verification status  |
| created_at      | TIMESTAMP    | Registration timestamp     |
| updated_at      | TIMESTAMP    | Last update timestamp      |

#### chat_rooms
Stores chat conversations (both direct and group).

| Column      | Type        | Description                      |
|-------------|-------------|----------------------------------|
| id          | SERIAL      | Primary key                      |
| name        | VARCHAR(100)| Group name (NULL for direct)     |
| room_type   | VARCHAR(20) | 'direct' or 'group'              |
| created_by  | INTEGER     | Foreign key to users             |
| created_at  | TIMESTAMP   | Creation timestamp               |
| updated_at  | TIMESTAMP   | Last update timestamp            |

#### chat_room_members
Junction table for many-to-many relationship between users and chat rooms.

| Column        | Type      | Description                |
|---------------|-----------|----------------------------|
| id            | SERIAL    | Primary key                |
| chat_room_id  | INTEGER   | Foreign key to chat_rooms  |
| user_id       | INTEGER   | Foreign key to users       |
| joined_at     | TIMESTAMP | Membership timestamp       |

**Unique constraint**: (chat_room_id, user_id)

#### messages
Stores all chat messages.

| Column        | Type      | Description                |
|---------------|-----------|----------------------------|
| id            | SERIAL    | Primary key                |
| chat_room_id  | INTEGER   | Foreign key to chat_rooms  |
| sender_id     | INTEGER   | Foreign key to users       |
| content       | TEXT      | Message content            |
| is_read       | BOOLEAN   | Read status                |
| created_at    | TIMESTAMP | Message timestamp          |

**Indexes**:
- chat_room_id (for fetching room messages)
- sender_id (for user message history)
- created_at DESC (for chronological ordering)

#### refresh_tokens
Stores refresh tokens for authentication.

| Column      | Type         | Description                |
|-------------|--------------|----------------------------|
| id          | SERIAL       | Primary key                |
| user_id     | INTEGER      | Foreign key to users       |
| token       | VARCHAR(500) | Unique refresh token       |
| expires_at  | TIMESTAMP    | Token expiration           |
| created_at  | TIMESTAMP    | Creation timestamp         |

### Relationships
```
users (1) ----< (M) chat_room_members (M) >---- (1) chat_rooms
users (1) ----< (M) messages >---- (1) chat_rooms
users (1) ----< (M) refresh_tokens
users (1) ----< (M) chat_rooms (created_by)
```

### CASCADE Behaviors

- **Delete chat room** → All messages and memberships deleted
- **Delete user** → Messages show "Deleted User", memberships removed
- **Delete user** → All refresh tokens deleted

---

## 🚢 Deployment

### Environment Variables for Production

Update `.env` for production:
```bash
DATABASE_URL=postgresql://user:password@production-host:5432/chatapp
SECRET_KEY=use-strong-random-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
DEBUG=False  # Important!
APP_NAME=RealtimeChatApp
```

### Docker Deployment (Optional)

**Create `Dockerfile`:**
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/src ./src

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Create `docker-compose.yml`:**
```yaml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_USER: chatuser
      POSTGRES_PASSWORD: chatpass
      POSTGRES_DB: chatapp
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - postgres
    environment:
      DATABASE_URL: postgresql://chatuser:chatpass@postgres:5432/chatapp

volumes:
  postgres_data:
```

**Run with Docker:**
```bash
docker-compose up -d
```

### Deployment Platforms

- **Heroku**: Follow [Heroku FastAPI guide](https://devcenter.heroku.com/articles/python-gunicorn)
- **AWS EC2**: Deploy on Ubuntu server with Nginx reverse proxy
- **DigitalOcean**: Use App Platform or Droplet
- **Railway**: Simple deployment with automatic SSL

---

## 🔧 Troubleshooting

### Common Issues

#### 1. Database Connection Error

**Error:** `could not connect to server`

**Solution:**
- Verify PostgreSQL is running
- Check DATABASE_URL in `.env`
- Ensure database `chatapp` exists
- Verify username and password
```bash
# Check if PostgreSQL is running
# On Windows:
services.msc

# On Mac:
brew services list

# On Linux:
sudo systemctl status postgresql
```

#### 2. Import Errors

**Error:** `ModuleNotFoundError: No module named 'src'`

**Solution:**
```bash
# Make sure you're in the backend directory
cd backend

# Run from backend directory
uvicorn src.main:app --reload
```

#### 3. Port Already in Use

**Error:** `[Errno 48] Address already in use`

**Solution:**
```bash
# Find process using port 8000
# On Mac/Linux:
lsof -i :8000

# On Windows:
netstat -ano | findstr :8000

# Kill the process
kill -9 <PID>
```

#### 4. WebSocket Connection Failed

**Error:** WebSocket closes immediately

**Solution:**
- Ensure backend is running
- Check token is valid (not expired)
- Verify WebSocket URL format: `ws://localhost:8000/ws/{token}`

#### 5. CORS Issues

**Error:** `Access to fetch blocked by CORS policy`

**Solution:**
Already configured in `main.py`, but ensure:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## 📖 Usage Guide

### Quick Start Tutorial

#### 1. Register Two Users

1. Open frontend: http://localhost:8501
2. Go to Login page
3. Switch to "Register" tab
4. Create User 1:
   - Username: alice
   - Email: alice@example.com
   - Password: password123
5. Create User 2 (open incognito browser):
   - Username: bob
   - Email: bob@example.com
   - Password: password123

#### 2. Send Direct Messages

1. Login as Alice
2. Go to Chat page
3. Enter Bob's user ID (find it in pgAdmin users table or API)
4. Click "Start Chat"
5. Type message and send
6. Login as Bob (other browser)
7. See Alice's message
8. Reply to Alice

#### 3. Create Group Chat

1. Login as Alice
2. Go to Groups page
3. Create group:
   - Name: "Team Chat"
   - Member IDs: Bob's ID, Charlie's ID (comma-separated)
4. Click "Create Group"
5. Send group message
6. Other members can see and reply

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Guidelines

- Write tests for new features
- Follow PEP 8 style guide
- Add docstrings to functions
- Update README if needed
- Include time/space complexity in docstrings

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 👤 Author

**Your Name**
- GitHub: [@aljebraschool](https://github.com/aljebraschool)

---

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- SQLAlchemy for the powerful ORM
- Streamlit for rapid UI development
- PostgreSQL for reliable data storage

---

## 📞 Support

If you have any questions or issues:
- Open an issue on GitHub

---

**Made with ❤️ and Python**