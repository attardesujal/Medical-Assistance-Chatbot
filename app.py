import streamlit as st
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import LlamaCpp
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from deep_translator import GoogleTranslator
import re

# ---------------------- Paths ---------------------- #
GGUF_MODEL_PATH = "models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
FAISS_DB_PATH = "vectorstore/db_faiss"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"

# ---------------------- Prompt Template ---------------------- #
CUSTOM_PROMPT_TEMPLATE = """
You are Medico, an intelligent and friendly AI medical assistant.

Your task is to answer questions in a clean, structured, markdown-friendly format like ChatGPT.

Follow these rules:
- Remove the None at the start of response only.
- Answer only what is asked (e.g., if asked about treatment, do not explain symptoms).
- Use numbered steps or bullet points for clarity.
- Make the tone helpful and human-like.
- Use headings (###) for different sections if needed.
- Use relevant emojis (🩺💊✔️⚠️) where helpful.
- Avoid introductions and closings like "Hi" or "Let me help you."

Context: {context}
Question: {question}

Start your response directly in markdown format. Be friendly, clear, and practical.
"""

# ---------------------- Load LLM ---------------------- #
@st.cache_resource
def load_llm():
    return LlamaCpp(
        model_path=GGUF_MODEL_PATH,
        temperature=0.4,
        max_tokens=1024,
        top_p=0.9,
        n_ctx=2048,
        n_batch=16,
        n_gpu_layers=-1,
        f16_kv=True,
        use_mlock=False,
        verbose=False
    )

# ---------------------- QA Chain ---------------------- #
@st.cache_resource
def setup_qa_chain():
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = FAISS.load_local(FAISS_DB_PATH, embeddings, allow_dangerous_deserialization=True)
    prompt = PromptTemplate(input_variables=["context", "question"], template=CUSTOM_PROMPT_TEMPLATE)
    llm = load_llm()
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=db.as_retriever(search_kwargs={"k": 3}),
        chain_type="stuff",
        return_source_documents=False,
        chain_type_kwargs={"prompt": prompt},
    )

# ---------------------- Translation ---------------------- #
def translate_and_format(text, target_lang):
    def clean_and_translate(line):
        if not line.strip():
            return ""
        match = re.match(r"^([➊-➒•✔️🔍❗🚫📌📝#]*)\s*(.*)", line)
        if match:
            prefix, content = match.groups()
        else:
            prefix, content = "", line
        try:
            translated = GoogleTranslator(source="auto", target=target_lang).translate(content.strip())
            return f"{prefix} {translated}".strip()
        except Exception as e:
            return f"{prefix} ⚠️ Translation error: {e}"
    lines = text.split("\n")
    translated_lines = [clean_and_translate(line) for line in lines]
    return "\n".join(translated_lines)

# ---------------------- Streamlit UI ---------------------- #
st.set_page_config(page_title="🩺 Medico Chatbot", layout="wide")

# Sidebar with language selection
with st.sidebar:
    st.image("0.png", width=200)
    st.title("🩺 Medico")
    st.markdown("Your AI Medical Assistant")
    language_map = {
        "English": "en",
        "Hindi": "hi",
        "Marathi": "mr",
        "Gujarati": "gu",
        "Tamil": "ta",
        "Telugu": "te",
        "Kannada": "kn",
        "Bengali": "bn",
        "Urdu": "ur",
    }
    selected_language = st.selectbox("🌐 Choose response language:", list(language_map.keys()), index=0)
    lang_code = language_map[selected_language]

# Main UI layout
st.markdown("<h1 style='text-align: center;'>💬 Medico - Your AI Medical Assistant</h1>", unsafe_allow_html=True)

qa_chain = setup_qa_chain()

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Chat input form
with st.form(key="chat_form", clear_on_submit=True):
    user_query = st.text_input("📝 Write your query here:")
    submitted = st.form_submit_button("Ask")

if submitted and user_query:
    with st.spinner("Thinking... 💭"):
        raw_response = qa_chain.run(user_query)
        if raw_response:
            translated = translate_and_format(raw_response, lang_code)
            st.session_state.chat_history.append(("🧑 You", user_query))
            st.session_state.chat_history.append(("🩺 Aarogya", translated))
        else:
            st.session_state.chat_history.append(("🩺 Aarogya", "⚠️ Sorry, I couldn't generate a response. Please try again."))

# Display chat history in styled bubbles
for speaker, msg in st.session_state.chat_history:
    if speaker == "🧑 You":
        st.markdown(f"<div style='background-color:#1e1e1e; color:white; padding:10px; border-radius:10px; margin:10px 0;'><strong>{speaker}:</strong><br>{msg}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div style='background-color:#2a2a2a; color:#c5f2ff; padding:10px; border-radius:10px; margin:10px 0;'><strong>{speaker}:</strong><br>{msg}</div>", unsafe_allow_html=True)

# Clear chat option
if st.button("🗑️ Clear Chat"):
    st.session_state.chat_history = []
