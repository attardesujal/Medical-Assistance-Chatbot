import streamlit as st
from deep_translator import GoogleTranslator

# Supported languages
LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Telugu": "te",
    "Tamil": "ta",
    "Sanskrit": "sa"
}

def translate_text(text, target_language):
    """Translates text to the selected language."""
    if target_language == "English":
        return text  # No need to translate

    translator = GoogleTranslator(source="auto", target=LANGUAGES[target_language])
    return translator.translate(text)

# Language Selection UI
def language_selector():
    selected_language = st.sidebar.selectbox("🌍 Select Language", list(LANGUAGES.keys()), index=0)
    return selected_language
