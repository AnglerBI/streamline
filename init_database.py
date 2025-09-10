#!/usr/bin/env python3
"""
Database initialization script for Daily Goals Generator
Run this script to create the required database tables in Neon PostgreSQL
"""

import os
import sys
from dotenv import load_dotenv
from database import db

def main():
    """Initialize the database with required tables"""
    load_dotenv()
    
    print("🗄️  Initializing Daily Goals Generator Database...")
    print("=" * 50)
    
    # Check if DATABASE_URL is set
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("❌ ERROR: DATABASE_URL environment variable not found.")
        print("Please set DATABASE_URL in your .env file.")
        sys.exit(1)
    
    print(f"📍 Database URL: {database_url[:30]}...")
    
    try:
        # Create all tables
        print("📋 Creating database tables...")
        db.create_tables()
        print("✅ Database tables created successfully!")
        
        print("\n📊 Database Schema Created:")
        print("  - users")
        print("  - questionnaire_responses") 
        print("  - daily_goals")
        
        print("\n🎉 Database initialization complete!")
        print("\nYou can now run your Streamlit app with:")
        print("  streamlit run app.py")
        
    except Exception as e:
        print(f"❌ Error initializing database: {str(e)}")
        print("\nPlease check:")
        print("  1. Your DATABASE_URL is correct")
        print("  2. Your database is accessible")
        print("  3. You have the required permissions")
        sys.exit(1)

if __name__ == "__main__":
    main()