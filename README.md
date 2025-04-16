🩺 Aarogya – Local Medical Chatbot
Aarogya is an intelligent medical assistant chatbot that runs completely offline using the Mistral 7B model via llama.cpp, with FAISS-based document search and multi-language support. It’s built with Streamlit, offers markdown-rich responses, and is optimized for GPU acceleration on local machines.

🚀 Features
✅ Runs entirely offline using a local .gguf Mistral model

✅ FAISS vector store for fast, context-aware medical retrieval

✅ ChatGPT-style markdown output (with headings, emojis, bullets)

✅ Multi-language support via Google Translate

✅ Streamlit UI with dark theme, logo, sidebar, and chat bubbles

✅ Custom prompt tuning for precise medical Q&A

 Project Structure
 📁 local_model
│
├── llama.cpp/                          # llama.cpp repo (used for local LLM)
│
├── models/
│   └── mistral/
│       └── mistral-7b-instruct-v0.1.Q4_K_M.gguf  # Local quantized LLM
│
├── vectorstore/
│   └── db_faiss/
│       ├── index.faiss                # FAISS index (large, don't upload to GitHub)
│       └── index.pkl                  # FAISS metadata
│
├── 0.png                              # Sidebar logo
├── 
└── app.py



