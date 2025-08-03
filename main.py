import streamlit as st
import spacy
import json
import os

from modules.users import process_user_mode
from modules.recruiters import process_recruiters_mode
from modules.admin import process_admin_mode
from modules.feedback import process_feedback_mode

nlp = spacy.load('en_core_web_sm')

USER_FILE = "users.json"

# -------- JSON Helpers --------
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as f:
            json.dump({}, f)

    with open(USER_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            # Fix for empty or corrupted file
            return {}

def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# -------- Authentication --------
def login(username, password):
    # Hardcoded role-based credentials
    if username == "Admin" and password == "Admin@123":
        return True, "admin"
    elif username == "Recruiter" and password == "Recruiter@123":
        return True, "recruiter"

    # Default user auth
    users = load_users()
    if username in users and users[username]['password'] == password:
        return True, "user"
    return False, None

def signup(username, password, email):
    users = load_users()
    if username in users:
        return False
    users[username] = {'password': password, 'email': email}
    save_users(users)
    return True

# -------- Main Menu Navigation --------
def mains_menu():
    st.sidebar.title("Navigation")
    st.sidebar.success(f"Logged in as: {st.session_state.username} ({st.session_state.role})")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.experimental_rerun()

    # Dynamic options based on role
    if st.session_state.role == "admin":
        app_mode = st.sidebar.selectbox("Choose an option", ["Admin"])
    elif st.session_state.role == "recruiter":
        app_mode = st.sidebar.selectbox("Choose an option", ["Recruiters"])
    elif st.session_state.role == "user":
        app_mode = st.sidebar.selectbox("Choose an option", ["Users"])
    else:
        st.error("Unknown role")
        return

    # Role-based processing
    if app_mode == "Users":
        process_user_mode()
    elif app_mode == "Recruiters":
        process_recruiters_mode()
    elif app_mode == "Admin":
        process_admin_mode()
    elif app_mode == "Feedback":
        process_feedback_mode()

# -------- App Entry Point --------
def main():
    st.set_page_config(page_title="Resume Ranker", layout="centered")

    # Initialize session
    if 'logged_in' not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""

    if st.session_state.logged_in:
        mains_menu()
        return

    # Login / Signup UI
    st.title("🔐 Login / Sign Up Page")
    choice = st.sidebar.selectbox("Select Option", ["Login", "Sign Up"])

    if choice == "Login":
        st.subheader("Login")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            success, role = login(username, password)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.role = role
                st.experimental_rerun()
            else:
                st.error("Invalid username or password.")

    elif choice == "Sign Up":
        st.subheader("Create New Account")
        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")

        def is_valid_email(email):
            import re
            pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
            return re.match(pattern, email) is not None

        if st.button("Sign Up"):
            if not new_user or not new_email or not new_pass:
                st.warning("⚠️ All fields are required.")
            elif not is_valid_email(new_email):
                st.error("❌ Please enter a valid email address.")
            elif signup(new_user, new_pass, new_email):
                st.success("✅ Account created successfully! Please log in.")
            else:
                st.warning("⚠️ Username already taken.")

if __name__ == '__main__':
    main()
