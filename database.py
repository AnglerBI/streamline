import os
from sqlalchemy import create_engine, Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
from datetime import datetime, date
import bcrypt
from dotenv import load_dotenv

load_dotenv()

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    
    user_id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    responses = relationship("QuestionnaireResponse", back_populates="user")
    goals = relationship("DailyGoal", back_populates="user")

class QuestionnaireResponse(Base):
    __tablename__ = 'questionnaire_responses'
    
    response_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    question_number = Column(Integer, nullable=False)
    question_text = Column(Text, nullable=False)
    response_value = Column(Text, nullable=False)
    submitted_at = Column(DateTime, default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="responses")

class DailyGoal(Base):
    __tablename__ = 'daily_goals'
    
    goal_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    goal_title = Column(String(100), nullable=False)
    goal_description = Column(Text)
    category = Column(String(50))
    generated_at = Column(DateTime, default=func.now())
    is_completed = Column(Boolean, default=False)
    
    # Relationships
    user = relationship("User", back_populates="goals")

class Database:
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL")
        if not self.database_url:
            raise ValueError("DATABASE_URL environment variable not found")
        
        self.engine = create_engine(self.database_url)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        
    def create_tables(self):
        """Create all tables in the database"""
        Base.metadata.create_all(bind=self.engine)
    
    def get_session(self):
        """Get a database session"""
        return self.SessionLocal()
    
    def create_user(self, email, password):
        """Register a new user"""
        session = self.get_session()
        try:
            # Check if user already exists
            existing_user = session.query(User).filter(User.email == email).first()
            if existing_user:
                return None, "User already exists"
            
            # Hash password
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            
            # Create new user
            new_user = User(email=email, password_hash=password_hash)
            session.add(new_user)
            session.commit()
            
            return new_user.user_id, "User created successfully"
        except Exception as e:
            session.rollback()
            return None, f"Error creating user: {str(e)}"
        finally:
            session.close()
    
    def verify_user(self, email, password):
        """Verify user login credentials"""
        session = self.get_session()
        try:
            user = session.query(User).filter(User.email == email).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                return user.user_id, "Login successful"
            return None, "Invalid email or password"
        except Exception as e:
            return None, f"Error verifying user: {str(e)}"
        finally:
            session.close()
    
    def save_responses(self, user_id, responses):
        """Save questionnaire responses"""
        session = self.get_session()
        try:
            # Clear existing responses for this user
            session.query(QuestionnaireResponse).filter(QuestionnaireResponse.user_id == user_id).delete()
            
            # Save new responses
            for question_number, (question_text, response_value) in responses.items():
                response = QuestionnaireResponse(
                    user_id=user_id,
                    question_number=question_number,
                    question_text=question_text,
                    response_value=str(response_value)
                )
                session.add(response)
            
            session.commit()
            return True, "Responses saved successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error saving responses: {str(e)}"
        finally:
            session.close()
    
    def get_user_responses(self, user_id):
        """Get user's questionnaire responses"""
        session = self.get_session()
        try:
            responses = session.query(QuestionnaireResponse).filter(
                QuestionnaireResponse.user_id == user_id
            ).order_by(QuestionnaireResponse.question_number).all()
            
            response_dict = {}
            for response in responses:
                response_dict[response.question_number] = {
                    'question_text': response.question_text,
                    'response_value': response.response_value
                }
            
            return response_dict
        except Exception as e:
            return {}
        finally:
            session.close()
    
    def has_completed_questionnaire(self, user_id):
        """Check if user has completed the questionnaire"""
        session = self.get_session()
        try:
            count = session.query(QuestionnaireResponse).filter(
                QuestionnaireResponse.user_id == user_id
            ).count()
            return count >= 10  # We have 10 questions
        except Exception as e:
            return False
        finally:
            session.close()
    
    def save_goals(self, user_id, goals):
        """Save generated goals for a user"""
        session = self.get_session()
        try:
            # Clear today's goals for this user
            today = date.today()
            session.query(DailyGoal).filter(
                DailyGoal.user_id == user_id,
                func.date(DailyGoal.generated_at) == today
            ).delete()
            
            # Save new goals
            for goal in goals:
                daily_goal = DailyGoal(
                    user_id=user_id,
                    goal_title=goal['title'],
                    goal_description=goal['description'],
                    category=goal['category']
                )
                session.add(daily_goal)
            
            session.commit()
            return True, "Goals saved successfully"
        except Exception as e:
            session.rollback()
            return False, f"Error saving goals: {str(e)}"
        finally:
            session.close()
    
    def get_today_goals(self, user_id):
        """Get today's goals for a user"""
        session = self.get_session()
        try:
            today = date.today()
            goals = session.query(DailyGoal).filter(
                DailyGoal.user_id == user_id,
                func.date(DailyGoal.generated_at) == today
            ).all()
            
            return [
                {
                    'goal_id': goal.goal_id,
                    'title': goal.goal_title,
                    'description': goal.goal_description,
                    'category': goal.category,
                    'is_completed': goal.is_completed
                }
                for goal in goals
            ]
        except Exception as e:
            return []
        finally:
            session.close()
    
    def mark_goal_complete(self, goal_id):
        """Mark a goal as completed"""
        session = self.get_session()
        try:
            goal = session.query(DailyGoal).filter(DailyGoal.goal_id == goal_id).first()
            if goal:
                goal.is_completed = True
                session.commit()
                return True, "Goal marked as completed"
            return False, "Goal not found"
        except Exception as e:
            session.rollback()
            return False, f"Error updating goal: {str(e)}"
        finally:
            session.close()
    
    def can_generate_goals_today(self, user_id):
        """Check if user can generate goals today (once per day limit)"""
        session = self.get_session()
        try:
            today = date.today()
            count = session.query(DailyGoal).filter(
                DailyGoal.user_id == user_id,
                func.date(DailyGoal.generated_at) == today
            ).count()
            return count == 0
        except Exception as e:
            return False
        finally:
            session.close()

# Initialize database instance
db = Database()