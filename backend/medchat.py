import os
from huggingface_hub import InferenceClient
from langchain_core.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.language_models import LLM
from pydantic import BaseModel, Field
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Hugging Face API credentials
HF_TOKEN = os.environ.get("HF_TOKEN")
HUGGINGFACE_REPO_ID = "mistralai/Mistral-7B-Instruct-v0.3"

# Step 1: Custom LLM Wrapper
class CustomHuggingFaceLLM(LLM, BaseModel):
    model_repo_id: str = Field(default=HUGGINGFACE_REPO_ID)
    token: str = Field(default=HF_TOKEN)

    def _call(self, prompt: str, stop=None, **kwargs):
        """ Call the Hugging Face inference client dynamically without storing it. """
        client = InferenceClient(model=self.model_repo_id, token=self.token)
        response = client.text_generation(prompt=prompt, max_new_tokens=512)
        return response

    @property
    def _identifying_params(self):
        return {"model_repo_id": self.model_repo_id}

    @property
    def _llm_type(self):
        return "huggingface_hub"

# Load LLM using Custom Wrapper
def load_llm():
    return CustomHuggingFaceLLM()

# Step 2: Custom Prompt
CUSTOM_PROMPT_TEMPLATE = """
You are a friendly and knowledgeable medical chatbot. When users ask about a disease, provide a **clear, user-friendly, and well-structured response** covering:

1. **What it is** (Explain in simple terms with an engaging tone).
2. **Types and subtypes** (If applicable, list common ones).
3. **Causes and risk factors** (Keep it simple and relatable).
4. **Diagnosis** (Explain how doctors detect the disease).
5. **Treatment options** (Mention common treatments, avoiding overwhelming details).
6. **Common medications** (List a few with basic effects and warnings).
7. **When to see a doctor** (Encourage users to seek medical advice if needed).

Your responses should be **easy to understand, engaging, and informative**—like a friendly expert explaining things to a non-medical person. Use bullet points, emojis (if appropriate), and simple language while maintaining accuracy. Avoid medical jargon unless necessary.

Context: {context}
Question: {question}

Start the answer directly. No small talk please.
"""

def set_custom_prompt(custom_prompt_template):
    return PromptTemplate(template=custom_prompt_template, input_variables=["context", "question"])

# Load FAISS Vector Database
DB_FAISS_PATH = "backend/vectorstore/db_faiss"
embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local(DB_FAISS_PATH, embedding_model, allow_dangerous_deserialization=True)

# Create QA Chain
qa_chain = RetrievalQA.from_chain_type(
    llm=load_llm(),
    chain_type="stuff",
    retriever=db.as_retriever(search_kwargs={'k': 3}),
    return_source_documents=True,
    chain_type_kwargs={'prompt': set_custom_prompt(CUSTOM_PROMPT_TEMPLATE)}
)

# Function to get chatbot response (For app.py)
def get_response(user_query):
    response = qa_chain.invoke({'query': user_query})

    # Extract response text
    answer = response["result"]

    # Extract and format source documents
    sources = []
    for doc in response["source_documents"]:
        source_info = f"📄 {os.path.basename(doc.metadata.get('source', 'Unknown'))}, Page {doc.metadata.get('page_label', 'N/A')}"
        sources.append(source_info)

    formatted_sources = "\n".join(sources) if sources else "No sources available."

    return answer, formatted_sources


# Run the chatbot (Standalone mode)
if __name__ == "__main__":
    user_query = input("Write Query Here: ")
    result, sources = get_response(user_query)

    print("\nRESULT:\n", result)
    print("\nSOURCE DOCUMENTS:\n", sources)
