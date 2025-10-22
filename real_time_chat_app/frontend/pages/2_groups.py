import streamlit as st
import sys
sys.path.append('..')
from utils.api_client import ChatAPI

st.set_page_config(page_title="Groups", page_icon="👥", layout="wide")

# Check if logged in
if not st.session_state.get("logged_in"):
    st.warning(" Please login first")
    st.stop()

api = st.session_state.api
current_user = st.session_state.user

st.title("👥 Group Chats")

# Sidebar - Group List
with st.sidebar:
    st.subheader("👥 Your Groups")
    
    if st.button("🔄 Refresh Groups"):
        st.rerun()
    
    # Get all groups
    try:
        groups = api.get_groups()
        
        if not groups:
            st.info("No groups yet. Create one!")
        else:
            for group in groups:
                with st.container():
                    if st.button(
                        f"👥 {group['name']}\n👤 {group['member_count']} members",
                        key=f"group_{group['id']}",
                        use_container_width=True
                    ):
                        st.session_state.selected_group = group
                        st.rerun()
                    
                    if group.get('last_message'):
                        st.caption(f"💬 {group['last_message'][:30]}...")
                    
                    st.divider()
    
    except Exception as e:
        st.error(f"Error loading groups: {e}")
    
    st.markdown("---")
    
    # Create Group Section
    st.subheader("➕ Create Group")
    
    with st.form("create_group_form"):
        group_name = st.text_input("Group Name")
        member_ids_input = st.text_input("Member IDs (comma-separated)", 
                                         placeholder="e.g., 2,3,4")
        submit = st.form_submit_button("Create Group", type="primary")
        
        if submit and group_name and member_ids_input:
            try:
                # Parse member IDs
                member_ids = [int(id.strip()) for id in member_ids_input.split(",")]
                
                result = api.create_group(group_name, member_ids)
                
                if "message" in result:
                    st.success(" Group created!")
                    st.rerun()
                else:
                    st.error(f" {result.get('detail', 'Failed to create group')}")
            
            except ValueError:
                st.error(" Invalid member IDs format")
            except Exception as e:
                st.error(f" Error: {e}")

# Main Group Chat Area
if 'selected_group' in st.session_state:
    group = st.session_state.selected_group
    group_id = group['id']
    group_name = group['name']
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        st.subheader(f"💬 {group_name}")
    
    with col2:
        st.metric("Members", group['member_count'])
    
    # Messages Container
    messages_container = st.container(height=400)
    
    # Load messages
    try:
        messages = api.get_group_messages(group_id, limit=50)
        
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
                                You • {msg['created_at'][:19]}
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
        group_message_input = st.text_input("Type a message...", key="group_message_input", 
                                           label_visibility="collapsed")
    
    with col2:
        send_group_button = st.button("Send", type="primary", use_container_width=True, 
                                     key="send_group")
    
    if send_group_button and group_message_input:
        try:
            result = api.send_group_message(group_id, group_message_input)
            st.success(" Sent!")
            st.rerun()
        except Exception as e:
            st.error(f"Error sending message: {e}")

else:
    st.info("Select a group from the sidebar or create a new one")