import streamlit as st

st.set_page_config(
    page_title="Real-Time Chat App",
    page_icon="💬",
    layout="wide"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'user' not in st.session_state:
    st.session_state.user = None

if 'api' not in st.session_state:
    from utils.api_client import ChatAPI
    st.session_state.api = ChatAPI()

# Main page
st.title("💬 Real-Time Chat Application")
st.markdown("---")

if not st.session_state.logged_in:
    st.warning(" Please login first")
    st.info("Go to **Login** page from the sidebar")
    
    st.markdown("""
    ## Features
    - 🔐 Secure authentication
    - 💬 One-to-one messaging
    - 👥 Group chats
    - ⚡ Real-time updates
    
    ## Get Started
    1. Click **Login** in the sidebar
    2. Create an account or login
    3. Start chatting!
    """)
else:
    user = st.session_state.user
    
    st.success(f"Welcome, **{user.get('username')}**!")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Username", user.get('username'))
    
    with col2:
        st.metric("Email", user.get('email'))
    
    with col3:
        if st.button("Logout", type="primary"):
            st.session_state.logged_in = False
            st.session_state.user = None
            st.session_state.api.token = None
            st.success("Logged out successfully!")
            st.rerun()
    
    st.markdown("---")
    st.info("Go to **Chat** page from the sidebar to start messaging!")