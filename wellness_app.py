import streamlit as st
from supabase_client import supabase_client
import re

# Configure Streamlit page
st.set_page_config(
    page_title="Wellness Tracker",
    page_icon="🌟",
    layout="centered",
    initial_sidebar_state="collapsed"
)

def initialize_session_state():
    """Initialize session state variables"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    if "page" not in st.session_state:
        st.session_state.page = "questionnaire"
    if "responses" not in st.session_state:
        st.session_state.responses = {}

def validate_phone(phone):
    """Basic phone number validation"""
    phone_pattern = r'^\+?1?[2-9]\d{2}[2-9]\d{2}\d{4}$'
    return re.match(phone_pattern, phone.replace('-', '').replace(' ', '').replace('(', '').replace(')', ''))

def validate_email(email):
    """Basic email validation"""
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_pattern, email)

def validate_password(password):
    """Basic password validation"""
    return len(password) >= 8

def render_questionnaire(editing=False):
    """Render the wellness questionnaire"""
    st.title("🌟 Wellness Tracker")

    if editing:
        st.subheader("Update Your Responses")
        # Load current responses if editing
        if st.session_state.user:
            current_responses = supabase_client.get_user_responses(st.session_state.user.id)
            if current_responses["success"] and current_responses["data"]:
                # Pre-populate form with current responses
                for key, value in current_responses["data"].items():
                    if key.startswith(('h', 'w', 'p', 'f')):
                        st.session_state.responses[key] = value
    else:
        st.write("Track your wellness across Health, Wealth, and Happiness dimensions.")

    # Health Section
    st.header("🏥 Health")

    h1 = st.radio(
        "Did you sleep 7+ hours last night?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="h1_sleep_7hrs",
        index=None if not editing else (0 if st.session_state.responses.get("h1_sleep_7hrs", True) else 1)
    )

    h2 = st.radio(
        "Did you eat 2+ servings of fruit/vegetables yesterday?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="h2_fruit_veg_2servings",
        index=None if not editing else (0 if st.session_state.responses.get("h2_fruit_veg_2servings", True) else 1)
    )

    h3 = st.radio(
        "Did you move for 20+ minutes yesterday?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="h3_moved_20mins",
        index=None if not editing else (0 if st.session_state.responses.get("h3_moved_20mins", True) else 1)
    )

    h4 = st.radio(
        "How often do you feel low energy during the day?",
        options=["Rarely", "Sometimes", "Often"],
        key="h4_low_energy_frequency",
        index=None if not editing else ["Rarely", "Sometimes", "Often"].index(st.session_state.responses.get("h4_low_energy_frequency", "Rarely"))
    )

    # Wealth Section
    st.header("💰 Wealth")

    w1 = st.radio(
        "Did you set aside any money last week?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="w1_saved_money",
        index=None if not editing else (0 if st.session_state.responses.get("w1_saved_money", True) else 1)
    )

    w2 = st.radio(
        "Would you feel secure if an emergency expense hit tomorrow?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="w2_emergency_secure",
        index=None if not editing else (0 if st.session_state.responses.get("w2_emergency_secure", True) else 1)
    )

    w3 = st.radio(
        "Did you spend on something you later regretted in the last month?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="w3_regretful_spending",
        index=None if not editing else (0 if st.session_state.responses.get("w3_regretful_spending", True) else 1)
    )

    # Happiness Section
    st.header("😊 Happiness")

    p1 = st.radio(
        "Did you do something just for yourself yesterday (read/walk/relax)?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="p1_personal_time",
        index=None if not editing else (0 if st.session_state.responses.get("p1_personal_time", True) else 1)
    )

    p2 = st.radio(
        "Did you connect with a close friend/family in the past week?",
        options=[True, False],
        format_func=lambda x: "Yes" if x else "No",
        key="p2_social_connection",
        index=None if not editing else (0 if st.session_state.responses.get("p2_social_connection", True) else 1)
    )

    p3 = st.radio(
        "How often do you feel overwhelmed by daily demands?",
        options=["Rarely", "Sometimes", "Often"],
        key="p3_overwhelmed_frequency",
        index=None if not editing else ["Rarely", "Sometimes", "Often"].index(st.session_state.responses.get("p3_overwhelmed_frequency", "Rarely"))
    )

    # Anchor Question
    st.header("🎯 Focus Area")

    f = st.radio(
        "If you could feel more 'in control' in one area next week, which would it be?",
        options=["Health", "Wealth", "Happiness"],
        key="f_focus_area",
        index=None if not editing else ["Health", "Wealth", "Happiness"].index(st.session_state.responses.get("f_focus_area", "Health"))
    )

    # Store responses
    responses = {
        "h1_sleep_7hrs": h1,
        "h2_fruit_veg_2servings": h2,
        "h3_moved_20mins": h3,
        "h4_low_energy_frequency": h4,
        "w1_saved_money": w1,
        "w2_emergency_secure": w2,
        "w3_regretful_spending": w3,
        "p1_personal_time": p1,
        "p2_social_connection": p2,
        "p3_overwhelmed_frequency": p3,
        "f_focus_area": f
    }

    st.session_state.responses = responses

    # Check if all questions are answered
    all_answered = all(value is not None for value in responses.values())

    # Action buttons
    col1, col2 = st.columns(2)

    if editing:
        with col1:
            if st.button("Save Changes", type="primary", use_container_width=True, disabled=not all_answered):
                if not all_answered:
                    st.error("Please answer all questions before saving.")
                else:
                    result = supabase_client.update_responses(st.session_state.user.id, responses)
                    if result["success"]:
                        st.success("Responses updated successfully!")
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"Error updating responses: {result['error']}")

        with col2:
            if st.button("Cancel", use_container_width=True):
                st.session_state.page = "dashboard"
                st.rerun()
    else:
        if st.button("Continue to Submit", type="primary", use_container_width=True, disabled=not all_answered):
            if not all_answered:
                st.error("Please answer all questions before continuing.")
            else:
                st.session_state.page = "auth"
                st.rerun()

    # Show progress indicator
    answered_count = sum(1 for value in responses.values() if value is not None)
    st.progress(answered_count / len(responses))
    st.caption(f"Questions answered: {answered_count}/{len(responses)}")

def render_auth():
    """Render authentication page"""
    st.title("📱 Submit Your Responses")

    # Toggle between login and registration
    auth_mode = st.radio("Select your option:", ["New User - Register", "Returning User - Login"], horizontal=True)

    with st.form("auth_form"):
        if auth_mode == "New User - Register":
            email = st.text_input("Email Address", placeholder="your@email.com")
            phone = st.text_input("Phone Number", placeholder="e.g., 555-123-4567")
            password = st.text_input("Password", type="password", help="Minimum 8 characters")
            submit_button = st.form_submit_button("Submit Responses", type="primary", use_container_width=True)
        else:
            email_or_phone = st.text_input("Email or Phone Number", placeholder="your@email.com or 555-123-4567", help="You can log in with either your email address or phone number")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Log In", type="primary", use_container_width=True)

        if submit_button:
            if auth_mode == "New User - Register":
                # Validate registration inputs
                if not validate_email(email):
                    st.error("Please enter a valid email address")
                    return

                if not validate_phone(phone):
                    st.error("Please enter a valid phone number")
                    return

                if not validate_password(password):
                    st.error("Password must be at least 8 characters long")
                    return

                # Register new user
                result = supabase_client.register_user(email, phone, password)
                if result["success"]:
                    user = result["user"]
                    st.session_state.user = user
                    st.session_state.authenticated = True

                    # Create user profile
                    profile_result = supabase_client.create_user_profile(user.id, phone, email)

                    # Save responses
                    responses_result = supabase_client.save_responses(user.id, st.session_state.responses)

                    if responses_result["success"]:
                        st.success("Registration successful! Redirecting to your dashboard...")
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error(f"Error saving responses: {responses_result['error']}")
                else:
                    st.error(f"Registration failed: {result['error']}")

            else:
                # Validate login inputs - allow either email or phone
                is_email = "@" in email_or_phone
                is_phone = validate_phone(email_or_phone)

                if not is_email and not is_phone:
                    st.error("Please enter a valid email address or phone number")
                    return

                if not validate_password(password):
                    st.error("Password must be at least 8 characters long")
                    return

                # Login existing user
                result = supabase_client.sign_in_user(email_or_phone, password)
                if result["success"]:
                    st.session_state.user = result["user"]
                    st.session_state.authenticated = True
                    st.success("Login successful! Redirecting to your dashboard...")
                    st.session_state.page = "dashboard"
                    st.rerun()
                else:
                    st.error(f"Login failed: {result['error']}")

def render_dashboard():
    """Render user dashboard with results"""
    if not st.session_state.authenticated or not st.session_state.user:
        st.session_state.page = "questionnaire"
        st.rerun()
        return

    # Get user responses
    responses_result = supabase_client.get_user_responses(st.session_state.user.id)

    if not responses_result["success"] or not responses_result["data"]:
        st.error("Could not load your responses")
        return

    responses = responses_result["data"]

    # Header
    st.title("🌟 Your Wellness Dashboard")
    st.write(f"Welcome back! Your focus area is: **{responses['f_focus_area']}**")

    # Health Section
    st.header("🏥 Health")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Sleep 7+ Hours", "Yes" if responses["h1_sleep_7hrs"] else "No")
        st.metric("Fruit/Vegetables", "Yes" if responses["h2_fruit_veg_2servings"] else "No")
    with col2:
        st.metric("Exercise 20+ Minutes", "Yes" if responses["h3_moved_20mins"] else "No")
        st.metric("Low Energy Frequency", responses["h4_low_energy_frequency"])

    # Wealth Section
    st.header("💰 Wealth")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Saved Money", "Yes" if responses["w1_saved_money"] else "No")
    with col2:
        st.metric("Emergency Secure", "Yes" if responses["w2_emergency_secure"] else "No")
    with col3:
        st.metric("Regretful Spending", "Yes" if responses["w3_regretful_spending"] else "No")

    # Happiness Section
    st.header("😊 Happiness")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Personal Time", "Yes" if responses["p1_personal_time"] else "No")
    with col2:
        st.metric("Social Connection", "Yes" if responses["p2_social_connection"] else "No")
    with col3:
        st.metric("Overwhelmed Frequency", responses["p3_overwhelmed_frequency"])

    # Action buttons
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Update My Responses", type="primary", use_container_width=True):
            st.session_state.page = "edit"
            st.rerun()

    with col2:
        if st.button("Change Password", use_container_width=True):
            st.session_state.page = "change_password"
            st.rerun()

    with col3:
        if st.button("Logout", use_container_width=True):
            supabase_client.sign_out()
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "questionnaire"
            st.success("Logged out successfully!")
            st.rerun()

def render_change_password():
    """Render password change page"""
    if not st.session_state.authenticated or not st.session_state.user:
        st.session_state.page = "questionnaire"
        st.rerun()
        return

    st.title("🔐 Change Password")

    with st.form("change_password_form"):
        current_password = st.text_input("Current Password", type="password")
        new_password = st.text_input("New Password", type="password", help="Minimum 8 characters")
        confirm_password = st.text_input("Confirm New Password", type="password")

        col1, col2 = st.columns(2)
        with col1:
            submit_button = st.form_submit_button("Update Password", type="primary", use_container_width=True)
        with col2:
            cancel_button = st.form_submit_button("Cancel", use_container_width=True)

        if cancel_button:
            st.session_state.page = "dashboard"
            st.rerun()

        if submit_button:
            # Validate inputs
            if not validate_password(new_password):
                st.error("New password must be at least 8 characters long")
                return

            if new_password != confirm_password:
                st.error("New password and confirmation do not match")
                return

            # Verify current password by attempting to sign in
            user_email = st.session_state.user.email
            verify_result = supabase_client.sign_in_user(user_email, current_password)

            if not verify_result["success"]:
                st.error("Current password is incorrect")
                return

            # Update password
            result = supabase_client.update_password(new_password)

            if result["success"]:
                st.success("Password updated successfully! Redirecting to dashboard...")
                st.session_state.page = "dashboard"
                st.rerun()
            else:
                st.error(f"Error updating password: {result['error']}")

def main():
    """Main application function"""
    initialize_session_state()

    # Page routing
    if st.session_state.page == "questionnaire":
        render_questionnaire()
    elif st.session_state.page == "auth":
        render_auth()
    elif st.session_state.page == "dashboard":
        render_dashboard()
    elif st.session_state.page == "edit":
        render_questionnaire(editing=True)
    elif st.session_state.page == "change_password":
        render_change_password()

if __name__ == "__main__":
    main()