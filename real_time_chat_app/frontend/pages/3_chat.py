import streamlit as st
import sys
sys.path.append('..')
from utils.api_client import ChatAPI
from datetime import datetime

st.set_page_config(page_title="Chat", page_icon="💬", layout="wide")

# Check if logged in
if not st.session_state.get("logged_in"):
    st.warning(" Please login first")
    st.stop()

api = st.session_state.api
current_user = st.session_state.user

st.title("💬 Direct Messages")

# Sidebar - Chat List
with st.sidebar:
    st.subheader("💬 Your Chats")
    
    if st.button("🔄 Refresh Chats"):
        st.rerun()
    
    # Get all chats
    try:
        chats = api.get_chats()
        
        if not chats:
            st.info("No chats yet. Start a new conversation!")
        else:
            for chat in chats:
                with st.container():
                    if st.button(
                        f"👤 {chat['other_user_username']}\n{chat.get('last_message', 'No messages')[:30]}...",
                        key=f"chat_{chat['other_user_id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_chat = chat
                        st.rerun()
                    
                    if chat.get('unread_count', 0) > 0:
                        st.caption(f" {chat['unread_count']} unread")
                    
                    st.divider()
    
    except Exception as e:
        st.error(f"Error loading chats: {e}")
    
    st.markdown("---")
    
    # New Chat Section
    st.subheader("➕ New Chat")
    new_chat_user_id = st.number_input("User ID", min_value=1, step=1, key="new_chat_id")
    
    if st.button("Start Chat", type="primary"):
        # Send a test message to create chat
        try:
            result = api.send_message(new_chat_user_id, " Hi!")
            st.success("Chat started!")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {e}")

# Main Chat Area
if 'selected_chat' in st.session_state:
    chat = st.session_state.selected_chat
    other_user_id = chat['other_user_id']
    other_username = chat['other_user_username']
    
    st.subheader(f"Chat with {other_username}")
    
    # Messages Container
    messages_container = st.container(height=400)
    
    # Load messages
    try:
        messages = api.get_chat_history(other_user_id, limit=50)
        
        with messages_container:
            if not messages:
                st.info("No messages yet. Start the conversation!")
            else:
                for msg in messages:
                    is_mine = msg['sender_id'] == current_user['id']
                    
                    if is_mine:
                        # My message (right aligned)
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"""
                            <div style='background-color: #0084ff; color: white; padding: 10px; 
                                        border-radius: 15px; margin: 5px 0; text-align: right;'>
                                {msg['content']}
                            </div>
                            <div style='text-align: right; font-size: 10px; color: gray;'>
                                {msg['created_at'][:19]}
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        # Their message (left aligned)
                        col1, col2 = st.columns([1, 3])
                        with col2:
                            st.markdown(f"""
                            <div style='background-color: #e4e6eb; color: black; padding: 10px; 
                                        border-radius: 15px; margin: 5px 0;'>
                                <b>{msg.get('sender_username', 'Unknown')}:</b><br>
                                {msg['content']}
                            </div>
                            <div style='font-size: 10px; color: gray;'>
                                {msg['created_at'][:19]}
                            </div>
                            """, unsafe_allow_html=True)
    
    except Exception as e:
        st.error(f"Error loading messages: {e}")
    
    # Message Input
    st.divider()
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        message_input = st.text_input("Type a message...", key="message_input", label_visibility="collapsed")
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    if send_button and message_input:
        try:
            result = api.send_message(other_user_id, message_input)
            st.success(" Sent!")
            st.rerun()
        except Exception as e:
            st.error(f"Error sending message: {e}")

else:
    st.info(" Select a chat from the sidebar or start a new one")