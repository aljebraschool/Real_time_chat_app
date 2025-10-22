import streamlit as st
import sys
sys.path.append('..')
from utils.api_client import ChatAPI

st.set_page_config(page_title="Login", page_icon="")

# Initialize API client
if 'api' not in st.session_state:
    st.session_state.api = ChatAPI()

api = st.session_state.api

st.title(" Login to Chat App")

# Tabs for Login and Register
tab1, tab2 = st.tabs(["Login", "Register"])

# Login Tab
with tab1:
    st.subheader("Login")
    
    login_username = st.text_input("Username or Email", key="login_username")
    login_password = st.text_input("Password", type="password", key="login_password")
    
    if st.button("Login", type="primary"):
        if login_username and login_password:
            with st.spinner("Logging in..."):
                result = api.login(login_username, login_password)
                
                if "error" in result:
                    st.error(f" {result['error']}")
                else:
                    st.session_state.user = result.get("user")
                    st.session_state.logged_in = True
                    st.success(" Login successful!")
                    st.balloons()
                    st.info(" Go to 'Chat' page from the sidebar")
        else:
            st.warning(" Please fill in all fields")

# Register Tab
with tab2:
    st.subheader("Create Account")
    
    reg_username = st.text_input("Username", key="reg_username")
    reg_email = st.text_input("Email", key="reg_email")
    reg_fullname = st.text_input("Full Name (Optional)", key="reg_fullname")
    reg_password = st.text_input("Password", type="password", key="reg_password")
    reg_password2 = st.text_input("Confirm Password", type="password", key="reg_password2")
    
    if st.button("Register", type="primary"):
        if reg_username and reg_email and reg_password:
            if reg_password != reg_password2:
                st.error(" Passwords don't match")
            elif len(reg_password) < 8:
                st.error("Password must be at least 8 characters")
            else:
                with st.spinner("Creating account..."):
                    try:
                        result = api.register(
                            username=reg_username,
                            email=reg_email,
                            password=reg_password,
                            full_name=reg_fullname
                        )
                        
                        if "message" in result:
                            st.success(" Account created successfully!")
                            st.info("Switch to 'Login' tab to sign in")
                        else:
                            st.error(f" {result.get('detail', 'Registration failed')}")
                    except Exception as e:
                        st.error(f" Error: {str(e)}")
        else:
            st.warning("Please fill in all required fields")

# Show current login status
st.divider()
if st.session_state.get("logged_in"):
    user = st.session_state.get("user", {})
    st.success(f" Logged in as: **{user.get('username')}**")
else:
    st.info("ℹ Not logged in")