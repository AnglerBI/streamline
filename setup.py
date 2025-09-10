#!/usr/bin/env python3
"""
Setup script for Daily Goals Generator
This script helps set up the environment and dependencies
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during {description}: {e.stderr}")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_path = ".env"
    if not os.path.exists(env_path):
        print("❌ .env file not found!")
        return False
    
    required_vars = ["DATABASE_URL", "OPENAI_API_KEY"]
    missing_vars = []
    
    with open(env_path, 'r') as f:
        content = f.read()
        for var in required_vars:
            if f"{var}=" not in content or f"{var}=your-" in content:
                missing_vars.append(var)
    
    if missing_vars:
        print(f"❌ Missing or incomplete environment variables: {', '.join(missing_vars)}")
        print("Please update your .env file with actual values.")
        return False
    
    print("✅ Environment variables configured")
    return True

def main():
    """Main setup function"""
    print("🚀 Daily Goals Generator Setup")
    print("=" * 40)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version.split()[0]} detected")
    
    # Install dependencies
    if not run_command("pip install -r requirements.txt", "Installing dependencies"):
        print("Please install dependencies manually: pip install -r requirements.txt")
        return
    
    # Check environment variables
    if not check_env_file():
        print("\n📝 Please configure your .env file:")
        print("  1. Set DATABASE_URL to your Neon PostgreSQL connection string")
        print("  2. Set OPENAI_API_KEY to your OpenAI API key")
        print("  3. Set SECRET_KEY to a random secret string")
        return
    
    # Initialize database
    if run_command("python init_database.py", "Initializing database"):
        print("\n🎉 Setup completed successfully!")
        print("\nNext steps:")
        print("  1. Run the app: streamlit run app.py")
        print("  2. Open your browser to the provided URL")
        print("  3. Create an account and start using the app!")
    else:
        print("\n❌ Database initialization failed.")
        print("Please run 'python init_database.py' manually.")

if __name__ == "__main__":
    main()