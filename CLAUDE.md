# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

This project uses `uv` for dependency management and virtual environment handling.

**Setup and Installation:**
```bash
uv sync  # Install dependencies and create/update virtual environment
```

**Database Initialization:**
```bash
python init_database.py  # Initialize database schema
# OR manually run schema.sql in Neon PostgreSQL console
```

**Running the Application:**
```bash
streamlit run app.py      # Run the Daily Goals Generator app
python setup.py          # Run automated setup script
```

**Development Environment:**
- Virtual environment is located at `.venv/`
- Python version: 3.13+
- Dependencies are managed via `pyproject.toml`
- Environment variables in `.env` file

## Architecture Overview

This is a comprehensive Daily Goals Generator application built with Streamlit that uses OpenAI to create personalized daily goals based on user questionnaire responses.

**Core Application Structure:**
- `app.py` - Main Streamlit application entry point
- `auth.py` - User authentication and session management
- `questionnaire.py` - 10-question user profile assessment
- `goals.py` - OpenAI integration for goal generation
- `database.py` - SQLAlchemy models and database operations

**Database Schema (Neon PostgreSQL):**
- `users` - User accounts with bcrypt password hashing
- `questionnaire_responses` - User profile responses (10 questions)
- `daily_goals` - AI-generated daily goals with completion tracking

**Application Flow:**
1. User registration/login with email/password
2. New users complete 10-question questionnaire
3. AI generates 3 personalized daily goals using OpenAI GPT-4o-mini
4. Users track progress by marking goals complete
5. New goals can be generated once per day

**Key Dependencies:**
- streamlit - Web application framework
- sqlalchemy - Database ORM
- openai - AI goal generation
- bcrypt - Password hashing
- psycopg2-binary - PostgreSQL adapter
- python-dotenv - Environment variable management

**Environment Variables Required:**
- `DATABASE_URL` - Neon PostgreSQL connection string
- `OPENAI_API_KEY` - OpenAI API key for goal generation
- `SECRET_KEY` - Session management secret

**Session Management:**
- Custom authentication using `st.session_state`
- User session persistence across app interactions
- Secure password hashing with bcrypt

**Goal Generation Logic:**
- Uses user questionnaire responses to create personalized prompts
- OpenAI GPT-4o-mini generates 3 goals per day
- Daily generation limit enforced at database level
- Goals categorized by user interests (Health, Career, Learning, etc.)