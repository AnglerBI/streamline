import streamlit as st
import bcrypt
from database import db

def hash_password(password):
    """Hash a password for storing"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password, hash_value):
    """Check if password matches hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hash_value.encode('utf-8'))

def create_session(user_id, email):
    """Create user session in Streamlit session state"""
    st.session_state.authenticated = True
    st.session_state.user_id = user_id
    st.session_state.user_email = email

def is_authenticated():
    """Check if user is authenticated"""
    return st.session_state.get('authenticated', False)

def get_current_user_id():
    """Get current user ID from session"""
    return st.session_state.get('user_id', None)

def logout():
    """Clear user session"""
    if 'authenticated' in st.session_state:
        del st.session_state.authenticated
    if 'user_id' in st.session_state:
        del st.session_state.user_id
    if 'user_email' in st.session_state:
        del st.session_state.user_email

def login_user(email, password):
    """Authenticate and login user"""
    user_id, message = db.verify_user(email, password)
    if user_id:
        create_session(user_id, email)
        return True, message
    return False, message

def register_user(email, password):
    """Register new user"""
    user_id, message = db.create_user(email, password)
    if user_id:
        create_session(user_id, email)
        return True, message
    return False, message

def show_login_page():
    """Display login/registration interface"""
    st.title("Daily Goals Generator")
    st.markdown("Welcome! Please login or create an account to get started.")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            login_button = st.form_submit_button("Login")
            
            if login_button:
                if email and password:
                    success, message = login_user(email, password)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("Please enter both email and password")
    
    with tab2:
        st.subheader("Create Account")
        with st.form("register_form"):
            reg_email = st.text_input("Email", key="reg_email")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm_password = st.text_input("Confirm Password", type="password", key="reg_confirm_password")
            register_button = st.form_submit_button("Create Account")
            
            if register_button:
                if reg_email and reg_password and reg_confirm_password:
                    if reg_password == reg_confirm_password:
                        if len(reg_password) >= 6:
                            success, message = register_user(reg_email, reg_password)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("Password must be at least 6 characters long")
                    else:
                        st.error("Passwords do not match")
                else:
                    st.error("Please fill in all fields")

def require_auth():
    """Decorator-like function to require authentication"""
    if not is_authenticated():
        show_login_page()
        return False
    return True