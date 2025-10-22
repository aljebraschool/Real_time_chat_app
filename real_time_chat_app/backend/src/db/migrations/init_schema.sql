--User Table
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(225) UNIQUE NOT NULL,
    email VARCHAR(225) UNIQUE NOT NULL,
    hashed_password VARCHAR(225) NOT NULL,
    full_name VARCHAR(225),
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Chat Rooms Table (for both 1-to-1 and group chats)
CREATE TABLE IF NOT EXISTS chat_rooms(
    id SERIAL PRIMARY KEY,
    name VARCHAR(225), -- NULL for 1-to-1, has value for groups
    room_type VARCHAR(100) NOT NULL CHECK (room_type IN ('direct', 'group')),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- Chat Room Members (many-to-many relationship)
CREATE TABLE IF NOT EXISTS chat_room_members(
    id SERIAL PRIMARY KEY,
    chat_room_id INTEGER REFERENCES chat_rooms(id) ON DELETE CASCADE,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(chat_room_id, user_id)
);

-- Messages Table
CREATE TABLE IF NOT EXISTS messages(
    id SERIAL PRIMARY KEY,
    chat_room_id INTEGER REFERENCES chat_rooms(id) ON DELETE CASCADE,
    sender_id INTEGER REFERENCES users(id) ON DELETE SET NULL,
    content TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Refresh Tokens Table (for authentication)
CREATE TABLE IF NOT EXISTS refresh_tokens(
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    token VARCHAR(500) UNIQUE NOT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_messages_chat_room ON messages(chat_room_id); -- get all messages find in this chat room id
CREATE INDEX IF NOT EXISTS idx_messages_sender ON messages(sender_id); -- use sender id to find all the messages they send
CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_chat_room_member_user ON chat_room_members(user_id); -- find chat room user is
CREATE INDEX IF NOT EXISTS idx_refresh_token_user ON refresh_tokens(user_id) 

