import streamlit as st
import requests

st.set_page_config(page_title="User System", layout="centered")

# Load CSS
def load_css():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

load_css()

API_URL = "http://127.0.0.1:8000"

st.markdown('<div class="main-card">', unsafe_allow_html=True)
st.markdown('<div class="title-text">🔐 User Management System</div>', unsafe_allow_html=True)

menu = st.radio("Select Option", ["Login", "Register", "Reset Password", "Delete Account"])

# ---------------- REGISTER ----------------
if menu == "Register":
    email = st.text_input("Email")
    year = st.number_input("Year of Birth", min_value=1900, max_value=2025)
    password = st.text_input("Password", type="password")
    conf = st.text_input("Confirm Password", type="password")

    if st.button("Register"):
        data = {
            "email": email,
            "year": year,
            "password": password,
            "conf_password": conf
        }

        response = requests.post(f"{API_URL}/register", json=data)

        if response.status_code == 200:
            st.success(response.json()["Status"])
        else:
            st.error(response.json()["detail"])


# ---------------- LOGIN ----------------
elif menu == "Login":
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        data = {"email": email, "password": password}
        response = requests.post(f"{API_URL}/login", json=data)

        if response.status_code == 200:
            st.success(response.json()["Status"])
        else:
            st.error("Login Failed")


# ---------------- RESET PASSWORD ----------------
elif menu == "Reset Password":
    email = st.text_input("Email")
    year = st.number_input("Year of Birth", min_value=1900, max_value=2025)
    new_password = st.text_input("New Password", type="password")

    if st.button("Reset"):
        data = {
            "email": email,
            "year": year,
            "new_password": new_password
        }

        response = requests.put(f"{API_URL}/reset_password/", json=data)

        if response.status_code == 200:
            st.success(response.json()["Result"])
        else:
            st.error("Verification Failed")


# ---------------- DELETE ACCOUNT ----------------
elif menu == "Delete Account":
    email = st.text_input("Email")

    if st.button("Delete"):
        data = {"email": email}
        response = requests.delete(f"{API_URL}/remove_acc", json=data)

        if response.status_code == 200:
            st.success(response.json()["Result"])
        else:
            st.error("Delete Failed")

st.markdown('</div>', unsafe_allow_html=True)