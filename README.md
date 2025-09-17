
# Aarogya – Local Medical Chatbot 

Aarogya is an intelligent, offline-first medical assistant chatbot. It leverages the power of the Mistral 7B model locally, ensuring your data remains private. With FAISS-based document search and multi-language support, it provides fast, context-aware medical information right on your machine.

-----

##  Key Features

   **Runs Entirely Offline:** No internet connection or API keys needed. Your conversations are completely private.
   **Intelligent & Context-Aware:** Utilizes a local Mistral 7B (`.gguf`) model via `llama.cpp` for high-quality responses.
   **FAISS Vector Store:** Enables rapid and relevant retrieval from your medical documents for accurate, context-aware answers.
   **Modern UI:** Built with Streamlit, featuring a user-friendly, ChatGPT-style interface with a dark theme, logo, and chat bubbles.
   **Multi-Language Support:** Integrated with Google Translate for seamless communication in various languages.
   **Customizable Prompts:** Specifically tuned to handle medical questions and answers with precision.
   **GPU Accelerated:** Optimized for high performance on local machines with GPU support.

-----
##  Technology Stack

  * **Large Language Model:** Mistral 7B (GGUF)
  * **Model Backend:** `llama.cpp` / `llama-cpp-python`
  * **Vector Database:** FAISS (Facebook AI Similarity Search)
  * **Web Framework:** Streamlit
  * **Translation:** Google Translate

-----

##  Project Structure

```
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
```

-----
##  Getting Started

Follow these steps to set up and run the project on your local machine.

### 1\. Prerequisites

  * Python 3.9+
  * Git

### 2\. Clone the Repository

```bash
git clone https://github.com/your-username/Aarogya.git
cd Aarogya
```

### 3\. Install Dependencies

Install the required Python packages.

```bash
pip install -r requirements.txt
```

### 4\. Download the LLM Model

The chatbot uses a quantized GGUF version of Mistral 7B for efficient local inference.

  * **Download the Model:**

      * Get the recommended `Q4_K_M` version (\~4.08 GB) from Hugging Face:
      * [**mistral-7b-instruct-v0.1.Q4\_K\_M.gguf**](https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/blob/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf)

  * **Place the Model:**

      * Create the necessary directories:
        ```bash
        mkdir -p models/mistral
        ```
      * Move the downloaded file to the correct location:
        `models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf`

### 5\. (Optional) GPU Acceleration

For the best performance, it is recommended to use hardware acceleration (GPU). The `llama-cpp-python` library should handle this by default if you have a compatible setup (like NVIDIA GPUs with CUDA).

For advanced tuning or specific hardware (e.g., Apple Metal), you can build `llama.cpp` manually. Follow the detailed instructions at the official repository: [**ggerganov/llama.cpp**](https://github.com/ggerganov/llama.cpp).

-----

##  Run the Application

Once the setup is complete, launch the Streamlit app with the following command:

```bash
streamlit run app.py
```

You can now open your browser and interact with the Aarogya medical chatbot\!
