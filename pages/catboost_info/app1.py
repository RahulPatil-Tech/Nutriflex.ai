
import os
import streamlit as st
import sqlite3
import hashlib
import time
import google.generativeai as genai

# Configure API key for Google Generative AI
os.environ["AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"] = "AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"
genai.configure(api_key=os.environ["AIzaSyB6RH6l9QkG-7YO4Pq6mkuac_lmSEAzHPc"])


# Generation configuration
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

# Database setup
conn = sqlite3.connect('users.db', check_same_thread=False)
c = conn.cursor()

# Create users table if it doesn't exist
def create_users_table():
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (user_id TEXT PRIMARY KEY, password TEXT)''')

# Insert user into database
def add_user(user_id, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('INSERT INTO users (user_id, password) VALUES (?, ?)', (user_id, hashed_password))
    conn.commit()

# Verify if user exists and password is correct
def verify_user(user_id, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT * FROM users WHERE user_id = ? AND password = ?', (user_id, hashed_password))
    return c.fetchone()

# Function to generate health tips using Google Generative AI
def generate_health_tips():
    prompt = "Give me some personalized health tips for maintaining a healthy lifestyle."
    
    # define model
    model = genai.GenerativeModel(model_name="gemini-1.5-flash",generation_config=generation_config,) 
    chat_session = model.start_chat(history=[])
    response = chat_session.send_message(prompt)
    return response.text.strip()
# Simulate recommendations based on user behavior
def get_personalized_recommendation(user_data):
    if user_data['calories'] > 2000:
        return "Consider reducing your calorie intake to meet your weight loss goals."
    elif user_data['steps'] < 8000:
        return "Try to increase your steps to meet your daily activity goal."
    else:
        return "You're on track! Keep up the good work."

# Function to display dashboard after login
def show_dashboard(user_id):
    st.title(f"Welcome, {user_id}!")
    
    # Example of user-specific health data (in a real application, fetch this from a database)
    user_health_data = {"calories": 1800, "steps": 7500, "goals": "Maintain weight"}

    # Display Health Data Overview
    st.subheader("Your Health Data Overview")
    st.write(f"**Daily Calorie Intake:** {user_health_data['calories']} kcal")
    st.write(f"**Steps Taken Today:** {user_health_data['steps']} steps")
    st.write(f"**Health Goal:** {user_health_data['goals']}")

    # Display health tips using Google Generative AI
    st.subheader("Personalized Health Tips")
    health_tips = generate_health_tips()
    st.write(health_tips)  # Show the generated health tips

    # Display personalized recommendation based on user data
    st.subheader("Personalized Recommendation")
    recommendation = get_personalized_recommendation(user_health_data)
    st.write(f"📋 {recommendation}")

# Main app functionality
def main():
    st.title("User Registration, Login, and Personalized Dashboard")

    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)

    create_users_table()  # Ensure the users table is created

    if choice == "Register":
        st.subheader("Create a New Account")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        
        if st.button("Register"):
            if password != password_confirm:
                st.error("Passwords do not match!")
            elif len(user_id) == 0 or len(password) == 0:
                st.error("User ID and Password cannot be empty!")
            else:
                try:
                    add_user(user_id, password)
                    st.success("Registration successful! You can now log in.")
                except sqlite3.IntegrityError:
                    st.error("User ID already exists. Try a different one.")
    
    elif choice == "Login":
        st.subheader("Login to Your Account")
        user_id = st.text_input("User ID")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if verify_user(user_id, password):
                st.success(f"Welcome, {user_id}!")
                time.sleep(1)  # Adding a small delay to simulate loading
                show_dashboard(user_id)  # Redirect to dashboard
            else:
                st.error("Invalid User ID or Password!")

if __name__ == "__main__":
    main()