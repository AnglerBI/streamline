# Wellness Tracker MVP

A simple Streamlit web application that captures user responses to 11 wellness questions across Health, Wealth, and Happiness dimensions, with Supabase backend for database and authentication.

## Features

- 11-question wellness survey across Health, Wealth, and Happiness
- User registration and authentication with phone/password
- Results dashboard with historical tracking
- Response editing with change history
- Row-level security for data privacy

## Quick Start

### Prerequisites

- Python 3.8+
- A Supabase project (already configured)

### Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Environment is already configured with your Supabase credentials in:
   - `.env` file for local development
   - `.streamlit/secrets.toml` for Streamlit deployment

### Running the Application

```bash
streamlit run wellness_app.py
```

The application will open in your browser at `http://localhost:8501`

## Database Schema

The application uses three main tables in Supabase:

- `user_profiles` - User profile information
- `responses` - Current user responses
- `response_history` - Historical changes (slowly changing dimension)

All tables have Row Level Security (RLS) enabled to ensure users can only access their own data.

## Usage Flow

1. **Landing Page**: Complete the 11-question wellness survey
2. **Registration/Login**: Provide phone number and password
3. **Dashboard**: View your wellness assessment results
4. **Edit Responses**: Update responses with automatic history tracking

## Application Structure

- `wellness_app.py` - Main Streamlit application with all UI components
- `supabase_client.py` - Supabase connection and database operations
- `requirements.txt` - Python dependencies
- `.env` - Environment variables (local development)
- `.streamlit/secrets.toml` - Streamlit secrets (deployment)

## Security Features

- Row Level Security (RLS) policies
- Password encryption via Supabase Auth
- Session management
- Input validation
- No data sharing between users

## Deployment

For Streamlit Cloud deployment:
1. Push code to GitHub repository
2. Connect repository to Streamlit Cloud
3. Secrets are already configured in `.streamlit/secrets.toml`
4. Deploy and share the URL

## Technical Details

- **Frontend**: Streamlit (Python web framework)
- **Backend**: Supabase (PostgreSQL + Auth)
- **Authentication**: Supabase Auth with phone/password
- **Database**: PostgreSQL with Row Level Security

## Troubleshooting

If you encounter issues:
1. Verify Supabase credentials in `.env` or secrets
2. Check that all database tables and policies are created
3. Ensure your Supabase project allows phone authentication
4. Check browser console for any JavaScript errors

For support, check the Supabase dashboard for logs and authentication settings.