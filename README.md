Aarogya – Local Medical Chatbot
Aarogya is an intelligent medical assistant chatbot that runs completely offline using the Mistral 7B model via llama.cpp, with FAISS-based document search and multi-language support. It’s built with Streamlit, offers markdown-rich responses, and is optimized for GPU acceleration on local machines.

 Features
 Runs entirely offline using a local .gguf Mistral model

 FAISS vector store for fast, context-aware medical retrieval

 ChatGPT-style markdown output (with headings, emojis, bullets)

 Multi-language support via Google Translate

 Streamlit UI with dark theme, logo, sidebar, and chat bubbles

 Custom prompt tuning for precise medical Q&A

 Project Structure
Aarogya2/
├── llama.cpp
├── models/
│   └── mistral/
│       └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
├── vectorstore/
│   └── db_faiss/
│       ├── index.faiss
│       └── index.pkl
│                   
└── app.py

 Model Download (Mistral 7B)
To run the chatbot locally, download the quantized GGUF model:

 [Mistral-7B-Instruct-v0.1.Q4_K_M.gguf - Hugging Face ](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF)

🔸 Recommended: Q4_K_M version (~4GB)
🔸 Place it in: models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf

llama-cpp-python handles the backend by default, but to build llama.cpp manually (for GPU tuning):
ggerganov/llama.cpp on GitHub

 Run the App
streamlit run app.py
