import streamlit as st
from components.chat import chat_interface
from components.theme import apply_theme
from components.language import language_selector

# Set page config
st.set_page_config(page_title="Aarogya - AI Health Assistant", page_icon="🩺", layout="wide")

# Apply Theme
apply_theme()

# Sidebar options (No Authentication)
st.sidebar.title("⚙️ Features")
page = st.sidebar.radio("Navigate", ["💬 Chatbot"])

# Select language
selected_language = language_selector()

# Load the selected page
if page == "💬 Chatbot":
    chat_interface()


