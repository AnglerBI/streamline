import os
import json
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from database import db
from auth import get_current_user_id
from questionnaire import get_user_profile_summary

load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_prompt(user_responses):
    """Generate the prompt for OpenAI based on user responses"""
    return f"""
Based on this user profile, generate exactly 3 daily goals in JSON format.

User Profile:
- Age Range: {user_responses.get('age_range', 'Not specified')}
- Occupation: {user_responses.get('occupation', 'Not specified')}
- Health Priority: {user_responses.get('health_priority', 'Not specified')}
- Daily Free Time: {user_responses.get('free_time', 'Not specified')} hours
- Main Challenge: {user_responses.get('challenge', 'Not specified')}
- Interest Categories: {user_responses.get('categories', 'Not specified')}
- Schedule Preference: {user_responses.get('schedule', 'Not specified')} person
- Stress Level: {user_responses.get('stress', 'Not specified')}/10
- Goal Difficulty: {user_responses.get('difficulty', 'Not specified')}
- Main Motivation: {user_responses.get('motivation', 'Not specified')}

Requirements:
1. Generate exactly 3 goals that can be completed today
2. Each goal should be specific, actionable, and realistic
3. Consider the user's available time, stress level, and preferences
4. Match the difficulty level to their preference
5. Include goals from their areas of interest when possible

Return ONLY a JSON array with this exact structure:
[
  {{
    "title": "Goal title (max 100 characters)",
    "description": "Detailed description with specific actions (max 300 characters)",
    "category": "One of: Health, Career, Learning, Relationships, Hobbies"
  }},
  {{
    "title": "Goal title (max 100 characters)",
    "description": "Detailed description with specific actions (max 300 characters)",
    "category": "One of: Health, Career, Learning, Relationships, Hobbies"
  }},
  {{
    "title": "Goal title (max 100 characters)",
    "description": "Detailed description with specific actions (max 300 characters)",
    "category": "One of: Health, Career, Learning, Relationships, Hobbies"
  }}
]

Make goals practical, motivating, and tailored to this specific user's profile.
"""

def get_daily_goals(user_responses):
    """Generate daily goals using OpenAI API"""
    try:
        prompt = generate_prompt(user_responses)
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a personal goal coach who creates achievable, motivating daily goals. Always respond with valid JSON only."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=800
        )
        
        # Extract and parse the JSON response
        content = response.choices[0].message.content.strip()
        
        # Remove any potential markdown formatting
        if content.startswith("```json"):
            content = content[7:]
        if content.endswith("```"):
            content = content[:-3]
        
        goals = json.loads(content)
        
        # Validate the response structure
        if not isinstance(goals, list) or len(goals) != 3:
            raise ValueError("Response must be a list of exactly 3 goals")
        
        for goal in goals:
            if not all(key in goal for key in ["title", "description", "category"]):
                raise ValueError("Each goal must have title, description, and category")
            
            # Trim to max lengths if needed
            goal["title"] = goal["title"][:100]
            goal["description"] = goal["description"][:300]
        
        return goals, None
        
    except json.JSONDecodeError as e:
        return None, f"Failed to parse AI response: {str(e)}"
    except Exception as e:
        return None, f"Error generating goals: {str(e)}"

def generate_daily_goals(user_id):
    """Main function to generate and save daily goals for a user"""
    try:
        # Check if user can generate goals today
        if not db.can_generate_goals_today(user_id):
            return False, "You can only generate goals once per day. Try again tomorrow!"
        
        # Get user's questionnaire responses
        user_responses = get_user_profile_summary(user_id)
        if not user_responses:
            return False, "Please complete the questionnaire first to generate personalized goals."
        
        # Generate goals using OpenAI
        goals, error = get_daily_goals(user_responses)
        if error:
            return False, error
        
        # Save goals to database
        success, message = db.save_goals(user_id, goals)
        if not success:
            return False, f"Failed to save goals: {message}"
        
        return True, "Daily goals generated successfully!"
        
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def format_goals_for_display(goals):
    """Format goals for display in the Streamlit UI"""
    if not goals:
        return []
    
    formatted_goals = []
    for goal in goals:
        formatted_goal = {
            'goal_id': goal.get('goal_id'),
            'title': goal.get('title', 'Untitled Goal'),
            'description': goal.get('description', 'No description available'),
            'category': goal.get('category', 'General'),
            'is_completed': goal.get('is_completed', False)
        }
        formatted_goals.append(formatted_goal)
    
    return formatted_goals

def show_dashboard():
    """Display the goals dashboard"""
    st.title("🎯 Your Daily Goals")
    
    user_id = get_current_user_id()
    if not user_id:
        st.error("User not authenticated")
        return
    
    # Get today's goals
    today_goals = db.get_today_goals(user_id)
    
    if not today_goals:
        st.info("You don't have any goals for today yet!")
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🚀 Generate My Daily Goals", type="primary"):
                with st.spinner("Generating your personalized goals..."):
                    success, message = generate_daily_goals(user_id)
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        with col2:
            if st.button("📝 Retake Questionnaire"):
                # Clear user responses to allow retaking questionnaire
                st.session_state.retake_questionnaire = True
                st.rerun()
    else:
        # Display existing goals
        st.markdown("### Today's Goals")
        
        goals_updated = False
        
        for i, goal in enumerate(today_goals):
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    # Goal content
                    status_emoji = "✅" if goal['is_completed'] else "⭕"
                    st.markdown(f"{status_emoji} **{goal['title']}**")
                    st.markdown(f"*Category: {goal['category']}*")
                    st.markdown(goal['description'])
                
                with col2:
                    if not goal['is_completed']:
                        if st.button("Mark Complete", key=f"complete_{goal['goal_id']}"):
                            success, message = db.mark_goal_complete(goal['goal_id'])
                            if success:
                                st.success("Goal completed! 🎉")
                                goals_updated = True
                            else:
                                st.error(f"Error: {message}")
                
                st.divider()
        
        # Refresh if goals were updated
        if goals_updated:
            st.rerun()
        
        # Show progress
        completed_count = sum(1 for goal in today_goals if goal['is_completed'])
        total_count = len(today_goals)
        
        st.markdown("### Progress")
        progress = completed_count / total_count if total_count > 0 else 0
        st.progress(progress)
        st.markdown(f"Completed: {completed_count}/{total_count} goals")
        
        if completed_count == total_count:
            st.balloons()
            st.success("🎉 Congratulations! You've completed all your goals for today!")
        
        # Option to retake questionnaire
        with st.expander("⚙️ Settings"):
            col1, col2 = st.columns([1, 1])
            
            with col1:
                if st.button("📝 Retake Questionnaire"):
                    st.session_state.retake_questionnaire = True
                    st.rerun()
            
            with col2:
                can_generate = db.can_generate_goals_today(user_id)
                if not can_generate:
                    st.info("New goals available tomorrow!")
                else:
                    if st.button("🔄 Generate New Goals"):
                        with st.spinner("Generating new goals..."):
                            success, message = generate_daily_goals(user_id)
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)

def check_daily_limit(user_id):
    """Check if user has reached daily goal generation limit"""
    return db.can_generate_goals_today(user_id)