**Aarogya – Local & Private Medical Chatbot**
Aarogya is an intelligent, offline-first medical assistant chatbot designed with privacy as a priority. It leverages the power of the Mistral 7B model running entirely on your local machine, ensuring that none of your sensitive data ever leaves your computer. With a FAISS-powered vector store for rapid document retrieval and multi-language support, Aarogya provides fast, contextually-aware medical information without needing an internet connection.

**Key Features**
 Runs Entirely Offline: No internet connection or API keys are needed. Your conversations are 100% private and secure.

 Intelligent & Context-Aware: Utilizes a local Mistral 7B (.gguf) model via llama.cpp for high-quality, human-like responses.

 FAISS Vector Store: Enables rapid and relevant information retrieval from your own medical documents for accurate, context-aware answers.

 Multi-Language Support: Integrated with Google Translate for seamless communication in various languages.

 Modern UI: Built with Streamlit, featuring a user-friendly, ChatGPT-style interface with a dark theme, logo, and chat bubbles.

 GPU Accelerated: Optimized for high-performance inference on local machines with NVIDIA (CUDA) or Apple (Metal) GPU support.

**How It Works**
Aarogya is built on a Retrieval-Augmented Generation (RAG) pipeline, which allows the chatbot to answer questions based on a local knowledge base.

Document Indexing (One-time setup): Medical documents are processed and converted into numerical representations (embeddings), which are then stored in a local FAISS vector database.

User Query: You ask a medical question in the chat interface.

Similarity Search: Your question is used to search the FAISS database for the most relevant text chunks from the indexed documents.

Context Injection: The relevant information retrieved from the documents is combined with your original question into a sophisticated prompt.

LLM Inference: This enhanced prompt is sent to the locally-running Mistral 7B model, which generates a comprehensive and contextually accurate answer.

**Technology Stack**
Large Language Model: Mistral 7B (GGUF format)

Model Backend: llama.cpp / llama-cpp-python

Vector Database: FAISS (Facebook AI Similarity Search)

Web Framework: Streamlit

Translation: Google Translate API

**Getting Started**
Follow these steps to set up and run the project on your local machine.

1. Prerequisites
Python 3.9+

Git

2. Installation
First, clone the repository and navigate into the project directory.

git clone [https://github.com/your-username/Aarogya.git](https://github.com/your-username/Aarogya.git)
cd Aarogya

Next, install all the required Python packages.

pip install -r requirements.txt

3. Model Setup
The chatbot uses a quantized GGUF version of Mistral 7B for efficient local inference.

a. Download the LLM Model

Get the recommended Q4_K_M version (~4.08 GB) from Hugging Face:

Download Link: mistral-7b-instruct-v0.1.Q4_K_M.gguf

b. Place the Model

Create the necessary directories:

mkdir -p models/mistral

Move the downloaded .gguf file to the correct location: models/mistral/

4. Run the Application
Once the setup is complete, launch the Streamlit app with the following command:

streamlit run app.py

You can now open your browser and interact with the Aarogya medical chatbot!

(Optional) GPU Acceleration
For the best performance, it is highly recommended to use hardware acceleration (GPU). The llama-cpp-python library is pre-configured to automatically use your GPU if you have a compatible setup (like NVIDIA GPUs with CUDA).

For advanced tuning or specific hardware (e.g., Apple Metal on Mac), you can build llama.cpp manually. Follow the detailed instructions at the official repository: ggerganov/llama.cpp.

**Project Structure**
Aarogya/
├── llama.cpp/              # Optional: For manual GPU tuning
├── models/
│   └── mistral/
│       └── mistral-7b-instruct-v0.1.Q4_K_M.gguf
├── vectorstore/
│   └── db_faiss/
│       ├── index.faiss
│       └── index.pkl
├── requirements.txt
└── app.py
