# aarogya
Here's your **README.md** file:  

---

## **🩺 Healthcare Assistance Chatbot**  

This project is a **medical assistance chatbot** designed to provide **health suggestions and medicine recommendations** based on user queries. The chatbot leverages **Hugging Face models, FAISS for vector search, and Streamlit for the web interface**.  

---

## **🚀 Features**  
✅ AI-powered chatbot using **Hugging Face models**  
✅ **FAISS vector search** for fast and efficient medical information retrieval  
✅ **Multi-language support** for diverse users  
✅ **Streamlit web interface** for an interactive user experience  

---

## **🛠️ Setup & Installation**  

### **1️⃣ Create a Hugging Face Token**  
To use Hugging Face models, you need an API token:  
- **Sign up or log in** to Hugging Face: [Hugging Face Website](https://huggingface.co/join)  
- Go to **Settings → Access Tokens**  
- Click **New Token** → Set **Read Access**  
- Copy the token and save it for later use.  

---

### **2️⃣ Prepare the FAISS Vector Store**  
- Ensure that the FAISS index (`db_faiss`) is saved in the **backend**.  

---

### **3️⃣ Run the Project**  
Once everything is set up, run the chatbot using:  
```bash
streamlit run app.py
```
This will start the chatbot interface in your browser.  

---

## **📂 Project Structure**  
```
📁 Medico-Chatbot
│── 📂 vectorstore
│   ├── db_faiss  # FAISS vector index
│── 📂 backend
│   ├── model.pkl  # Pickle file for NLP model
│── app.py  # Streamlit web app
│── requirements.txt  # Dependencies
│── README.md  # Project documentation
