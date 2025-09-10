import streamlit as st
from auth import is_authenticated, show_login_page, logout, get_current_user_id
from questionnaire import show_questionnaire
from goals import show_dashboard
from database import db

# Page configuration
st.set_page_config(
    page_title="Daily Goals Generator",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def initialize_database():
    """Initialize database tables if they don't exist"""
    try:
        db.create_tables()
        return True
    except Exception as e:
        st.error(f"Database initialization failed: {str(e)}")
        return False

def main():
    """Main application logic"""
    
    # Initialize database
    if not initialize_database():
        st.stop()
    
    # Initialize session state
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Check authentication
    if not is_authenticated():
        show_login_page()
        return
    
    # User is authenticated - show main app
    user_id = get_current_user_id()
    
    # Sidebar with user info and logout
    with st.sidebar:
        st.markdown("### Welcome!")
        st.markdown(f"**User ID:** {user_id}")
        st.markdown(f"**Email:** {st.session_state.get('user_email', 'Unknown')}")
        
        st.markdown("---")
        
        if st.button("🚪 Logout", use_container_width=True):
            logout()
            st.rerun()
        
        st.markdown("---")
        st.markdown("### About")
        st.markdown("This app generates personalized daily goals based on your profile and preferences.")
    
    # Check if user wants to retake questionnaire
    if st.session_state.get('retake_questionnaire', False):
        # Clear previous responses and show questionnaire
        st.session_state.retake_questionnaire = False
        show_questionnaire()
        return
    
    # Check if user has completed questionnaire
    has_completed = db.has_completed_questionnaire(user_id)
    
    if not has_completed:
        # Show questionnaire for new users
        show_questionnaire()
    else:
        # Show dashboard with goals
        show_dashboard()

if __name__ == "__main__":
    main()