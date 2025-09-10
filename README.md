# Daily Goals Generator 🎯

A Streamlit application that generates personalized daily goals using OpenAI based on user preferences and profile information.

## Features

- **User Authentication**: Secure login/registration system
- **Personal Questionnaire**: 10-question profile assessment
- **AI-Powered Goals**: Personalized daily goals using OpenAI GPT-4o-mini
- **Progress Tracking**: Mark goals as completed and track progress
- **Daily Limits**: One goal generation per day to encourage consistency
- **PostgreSQL Integration**: Secure data storage with Neon database

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python 3.13+
- **Database**: Neon PostgreSQL
- **AI**: OpenAI GPT-4o-mini
- **Authentication**: Custom bcrypt implementation
- **Dependencies**: SQLAlchemy, python-dotenv, psycopg2

## Quick Start

### 1. Clone and Setup
```bash
git clone <repository-url>
cd streamline
```

### 2. Install Dependencies
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

### 3. Environment Configuration
Create a `.env` file with your credentials:
```bash
DATABASE_URL=postgresql://username:password@host:port/database
OPENAI_API_KEY=your-openai-api-key
SECRET_KEY=your-random-secret-key
```

### 4. Database Setup
Run the SQL schema in your Neon PostgreSQL database:
```bash
# Execute schema.sql in your Neon database console
# Or run the Python initialization script:
python init_database.py
```

### 5. Run the Application
```bash
streamlit run app.py
```

## Application Flow

1. **Registration/Login**: Users create accounts or sign in
2. **Questionnaire**: New users complete a 10-question profile assessment
3. **Goal Generation**: AI generates 3 personalized daily goals
4. **Progress Tracking**: Users mark goals as completed
5. **Daily Cycle**: New goals can be generated once per day

## Project Structure

```
streamline/
├── app.py                 # Main Streamlit application
├── database.py           # SQLAlchemy models and database operations
├── auth.py              # Authentication functions
├── questionnaire.py     # Question definitions and handlers
├── goals.py            # OpenAI integration and goal generation
├── init_database.py    # Database initialization script
├── setup.py           # Automated setup script
├── schema.sql         # SQL schema for manual database setup
├── requirements.txt   # Python dependencies
├── .env              # Environment variables (create this)
└── README.md         # This file
```

## Database Schema

### users
- `user_id` (SERIAL PRIMARY KEY)
- `email` (VARCHAR UNIQUE)
- `password_hash` (VARCHAR)
- `created_at` (TIMESTAMP)

### questionnaire_responses
- `response_id` (SERIAL PRIMARY KEY)
- `user_id` (INTEGER FOREIGN KEY)
- `question_number` (INTEGER)
- `question_text` (TEXT)
- `response_value` (TEXT)
- `submitted_at` (TIMESTAMP)

### daily_goals
- `goal_id` (SERIAL PRIMARY KEY)
- `user_id` (INTEGER FOREIGN KEY)
- `goal_title` (VARCHAR)
- `goal_description` (TEXT)
- `category` (VARCHAR)
- `generated_at` (TIMESTAMP)
- `is_completed` (BOOLEAN)

## Questionnaire Questions

1. Age Range (selectbox)
2. Occupation (text input)
3. Health Priority (radio buttons)
4. Daily Free Time (slider, 0-8 hours)
5. Main Challenge (text area)
6. Preferred Categories (multiselect)
7. Schedule Preference (radio buttons)
8. Stress Level (slider, 1-10)
9. Goal Difficulty Preference (radio buttons)
10. Biggest Motivation (text area)

## Development

### Running Tests
```bash
# Add your test commands here
python -m pytest
```

### Code Style
```bash
# Add linting commands here
black .
flake8 .
```

## Deployment

1. Set up a Neon PostgreSQL database
2. Configure environment variables on your hosting platform
3. Install dependencies
4. Run database initialization
5. Deploy with your preferred platform (Streamlit Cloud, Heroku, etc.)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Neon PostgreSQL connection string | Yes |
| `OPENAI_API_KEY` | OpenAI API key for goal generation | Yes |
| `SECRET_KEY` | Secret key for session management | Yes |

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details
