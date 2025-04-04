import streamlit as st

def apply_theme():
    """Applies light or dark theme based on user selection."""
    theme_mode = st.sidebar.radio("🌓 Choose Theme", ["Light", "Dark"], index=1)

    if theme_mode == "Dark":
        dark_mode_css = """
        <style>
            body { background-color: #1E1E1E; color: white; }
            .stTextInput, .stButton, .stRadio { color: white; }
            .stTextInput>div>div>input { background-color: #333333; color: white; }
            .stButton>button { background-color: #444; color: white; border: 1px solid white; }
        </style>
        """
        st.markdown(dark_mode_css, unsafe_allow_html=True)

    else:
        light_mode_css = """
        <style>
            body { background-color: #FFFFFF; color: black; }
            .stTextInput, .stButton, .stRadio { color: black; }
            .stTextInput>div>div>input { background-color: #F0F0F0; color: black; }
            .stButton>button { background-color: #E0E0E0; color: black; border: 1px solid black; }
        </style>
        """
        st.markdown(light_mode_css, unsafe_allow_html=True)

    return theme_mode
