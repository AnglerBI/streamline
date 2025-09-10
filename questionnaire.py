import streamlit as st
from database import db
from auth import get_current_user_id

# Define all 10 questions
QUESTIONS = {
    1: {
        "text": "What is your age range?",
        "type": "selectbox",
        "options": ["18-24", "25-34", "35-44", "45-54", "55+"],
        "key": "age_range"
    },
    2: {
        "text": "What is your occupation?",
        "type": "text_input",
        "key": "occupation"
    },
    3: {
        "text": "How important is health and wellness to you?",
        "type": "radio",
        "options": ["Very Important", "Important", "Somewhat Important", "Not Important"],
        "key": "health_priority"
    },
    4: {
        "text": "How many hours of free time do you have daily?",
        "type": "slider",
        "min_value": 0,
        "max_value": 8,
        "value": 2,
        "key": "free_time"
    },
    5: {
        "text": "What is your main daily challenge? (max 200 characters)",
        "type": "text_area",
        "max_chars": 200,
        "key": "challenge"
    },
    6: {
        "text": "Which categories interest you most? (Select all that apply)",
        "type": "multiselect",
        "options": ["Health", "Career", "Learning", "Relationships", "Hobbies"],
        "key": "categories"
    },
    7: {
        "text": "Are you more of a morning or evening person?",
        "type": "radio",
        "options": ["Morning", "Evening", "Both"],
        "key": "schedule"
    },
    8: {
        "text": "What is your current stress level? (1 = very low, 10 = very high)",
        "type": "slider",
        "min_value": 1,
        "max_value": 10,
        "value": 5,
        "key": "stress"
    },
    9: {
        "text": "What difficulty level do you prefer for your goals?",
        "type": "radio",
        "options": ["Easy", "Medium", "Challenging"],
        "key": "difficulty"
    },
    10: {
        "text": "What motivates you most? (max 200 characters)",
        "type": "text_area",
        "max_chars": 200,
        "key": "motivation"
    }
}

def display_question(question_number, question_data):
    """Display a single question and return the response"""
    st.markdown(f"### Question {question_number}")
    st.markdown(f"**{question_data['text']}**")
    
    response = None
    
    if question_data["type"] == "selectbox":
        response = st.selectbox(
            "Select an option:",
            question_data["options"],
            key=f"q{question_number}_{question_data['key']}"
        )
    
    elif question_data["type"] == "text_input":
        response = st.text_input(
            "Your answer:",
            key=f"q{question_number}_{question_data['key']}"
        )
    
    elif question_data["type"] == "radio":
        response = st.radio(
            "Choose one:",
            question_data["options"],
            key=f"q{question_number}_{question_data['key']}"
        )
    
    elif question_data["type"] == "slider":
        response = st.slider(
            "Select value:",
            min_value=question_data["min_value"],
            max_value=question_data["max_value"],
            value=question_data["value"],
            key=f"q{question_number}_{question_data['key']}"
        )
    
    elif question_data["type"] == "text_area":
        response = st.text_area(
            "Your answer:",
            max_chars=question_data.get("max_chars", 500),
            key=f"q{question_number}_{question_data['key']}"
        )
    
    elif question_data["type"] == "multiselect":
        response = st.multiselect(
            "Select all that apply:",
            question_data["options"],
            key=f"q{question_number}_{question_data['key']}"
        )
    
    return response

def validate_response(question_number, response):
    """Validate a question response"""
    question_data = QUESTIONS[question_number]
    
    if question_data["type"] == "text_input" and not response.strip():
        return False, "Please provide an answer"
    
    if question_data["type"] == "text_area" and not response.strip():
        return False, "Please provide an answer"
    
    if question_data["type"] == "multiselect" and len(response) == 0:
        return False, "Please select at least one option"
    
    return True, ""

def show_questionnaire():
    """Display the complete questionnaire interface"""
    st.title("🎯 Personal Goal Questionnaire")
    st.markdown("Please answer these 10 questions to help us generate personalized daily goals for you.")
    
    # Initialize session state for questionnaire if not exists
    if 'questionnaire_step' not in st.session_state:
        st.session_state.questionnaire_step = 1
        st.session_state.questionnaire_responses = {}
    
    current_step = st.session_state.questionnaire_step
    
    # Show progress bar
    progress = current_step / len(QUESTIONS)
    st.progress(progress)
    st.markdown(f"Progress: {current_step}/{len(QUESTIONS)}")
    
    # Display current question
    if current_step <= len(QUESTIONS):
        question_data = QUESTIONS[current_step]
        
        # Show previous responses for context (if any)
        if current_step > 1:
            with st.expander("Previous Answers", expanded=False):
                for i in range(1, current_step):
                    prev_q = QUESTIONS[i]
                    prev_response = st.session_state.questionnaire_responses.get(i, "Not answered")
                    st.write(f"**Q{i}:** {prev_q['text']}")
                    st.write(f"**Answer:** {prev_response}")
        
        # Display current question
        with st.container():
            response = display_question(current_step, question_data)
            
            # Navigation buttons
            col1, col2, col3 = st.columns([1, 1, 1])
            
            with col1:
                if current_step > 1:
                    if st.button("← Previous", key="prev_btn"):
                        st.session_state.questionnaire_step -= 1
                        st.rerun()
            
            with col2:
                st.write("")  # Spacer
            
            with col3:
                if current_step < len(QUESTIONS):
                    if st.button("Next →", key="next_btn"):
                        # Validate current response
                        is_valid, error_msg = validate_response(current_step, response)
                        if is_valid:
                            st.session_state.questionnaire_responses[current_step] = response
                            st.session_state.questionnaire_step += 1
                            st.rerun()
                        else:
                            st.error(error_msg)
                else:
                    if st.button("Submit Questionnaire", key="submit_btn", type="primary"):
                        # Validate current response
                        is_valid, error_msg = validate_response(current_step, response)
                        if is_valid:
                            st.session_state.questionnaire_responses[current_step] = response
                            # Submit to database
                            submit_questionnaire()
                        else:
                            st.error(error_msg)

def submit_questionnaire():
    """Submit questionnaire responses to database"""
    user_id = get_current_user_id()
    if not user_id:
        st.error("User not authenticated")
        return
    
    # Prepare responses for database
    responses_for_db = {}
    for question_num, response in st.session_state.questionnaire_responses.items():
        question_text = QUESTIONS[question_num]["text"]
        responses_for_db[question_num] = (question_text, response)
    
    # Save to database
    success, message = db.save_responses(user_id, responses_for_db)
    
    if success:
        st.success("✅ Questionnaire completed successfully!")
        st.balloons()
        
        # Clear questionnaire state
        if 'questionnaire_step' in st.session_state:
            del st.session_state.questionnaire_step
        if 'questionnaire_responses' in st.session_state:
            del st.session_state.questionnaire_responses
        
        # Redirect to dashboard
        st.info("Redirecting to your dashboard...")
        st.rerun()
    else:
        st.error(f"Error saving questionnaire: {message}")

def process_questionnaire(responses):
    """Process questionnaire responses into a format suitable for goal generation"""
    processed = {}
    
    for question_num, response in responses.items():
        question_key = QUESTIONS[question_num]["key"]
        
        # Handle different response types
        if isinstance(response, list):  # multiselect
            processed[question_key] = ", ".join(response)
        else:
            processed[question_key] = str(response)
    
    return processed

def get_user_profile_summary(user_id):
    """Get a formatted summary of user's questionnaire responses"""
    responses = db.get_user_responses(user_id)
    
    if not responses:
        return None
    
    # Convert to our expected format
    processed_responses = {}
    for question_num, response_data in responses.items():
        question_key = QUESTIONS[question_num]["key"]
        processed_responses[question_key] = response_data["response_value"]
    
    return processed_responses