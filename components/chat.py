import streamlit as st
from backend.medchat import get_response

# Chatbot UI
def chat_interface():
    st.title("🩺 Aarogya - Your AI Health Assistant")
    st.markdown("Aarogya provides AI-powered medical guidance. Ask your health-related queries below.")

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display previous messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    user_input = st.chat_input("Ask Aarogya about health...")

    if user_input:
        # Display user message
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Get chatbot response (ignoring sources)
        answer, _ = get_response(user_input)

        # Display chatbot message
        st.session_state.messages.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(f"**🏥 Medical Advice:**\n\n{answer}")
