import streamlit as st
import json
import os
from modules.mains import mains_menu # type: ignore
# JSON file to store user data
USER_FILE = "users.json"

# Load users from JSON file
def load_users():
    if not os.path.exists(USER_FILE):
        with open(USER_FILE, 'w') as f:
            json.dump({}, f)
    with open(USER_FILE, 'r') as f:
        return json.load(f)

# Save users to JSON file
def save_users(users):
    with open(USER_FILE, 'w') as f:
        json.dump(users, f, indent=4)

# Login logic
def login(username, password):
    users = load_users()
    return username in users and users[username]['password'] == password

# Sign up logic
def signup(username, password, email):
    users = load_users()
    if username in users:
        return False
    users[username] = {'password': password, 'email': email}
    save_users(users)
    return True

def main():
    st.set_page_config(page_title="Login / Sign Up", layout="centered")
    st.title(" Login / Sign Up Page")

    choice = st.sidebar.selectbox("Select Option", ["Login", "Sign Up"])

    if choice == "Login":
        st.subheader("Login")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login(username, password):
                st.success(f"Welcome back, {username}!")
                mains_menu()
            else:
                st.error("Invalid username or password.")

    elif choice == "Sign Up":
        st.subheader("Create New Account")

        new_user = st.text_input("Username")
        new_email = st.text_input("Email")
        new_pass = st.text_input("Password", type="password")

        if st.button("Sign Up"):
            if signup(new_user, new_pass, new_email):
                st.success("Account created successfully! You can now log in.")
            else:
                st.warning("Username already taken.")

if __name__ == '__main__':
    main()
