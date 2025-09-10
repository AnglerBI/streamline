import os
import streamlit as st
import pandas as pd
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the connection string from the environment variable
conn_string = os.getenv("DATABASE_URL")

if not conn_string:
    st.error("DATABASE_URL environment variable not found. Please check your .env file.")
    st.stop()

conn = None

try:
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(conn_string)
    st.success("Connection successful!")

    # Example query to fetch data
    query = "SELECT * FROM books LIMIT 10;"  # Replace with actual table name
    df = pd.read_sql_query(query, conn)

    # Display the data in Streamlit
    st.dataframe(df)

except Exception as e:
    st.error(f"Connection failed: {str(e)}")
    
finally:
    if conn:
        conn.close()