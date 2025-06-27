# 🩺 MediGPT – AI-Powered Healthcare Chatbot

MediGPT is a full-stack AI chatbot that enables users to upload healthcare-related PDF documents and ask natural language questions to retrieve contextual answers. It integrates **LangChain**, **Amazon Bedrock**, and **Chroma** on the backend, with a **React** frontend for interaction.

---

## 🚀 Features

- 💬 Ask health-related questions using natural language
- 📄 Upload your own PDF documents (e.g., medical reports, guidelines)
- 🧠 Uses Amazon Bedrock for LLM and embeddings
- 🔍 Vector store powered by ChromaDB (persisted)
- 🌐 Built with FastAPI backend and React frontend
- 🔄 Live ingestion of newly uploaded PDFs without restarting the app

---

## 🛠️ Tech Stack

| Frontend              | Backend             | AI & Vector DB       |
|-----------------------|---------------------|-----------------------|
| React (Vite)          | FastAPI (Python)    | LangChain + Bedrock   |
| CSS Modules           | Uvicorn             | ChromaDB (vectorstore)|
| Axios / Fetch API     | CORS Middleware     | Bedrock Embeddings    |

---

## 📁 Project Structure
```bash
MediGPT/
│
├── backend/
│ ├── api.py # FastAPI app (main backend logic)
│ ├── utils/
│ │ └── ingest.py # Ingestion and embedding of PDFs
│ └── uploads/ # Uploaded PDFs
│
├── frontend/
│ ├── src/
│ │ ├── App.js
│ │ ├── components/
│ │ │ ├── ChatBox.js
│ │ │ ├── PdfUpload.js
│ │ │ ├── ChatBox.css
│ │ │ └── ...
│ └── public/
│
├── rag/
│ └── vectorstore/ # Chroma vectorstore (persistent)
├── .env # AWS Bedrock credentials


## Frontend (React)

cd frontend
npm install
npm start

## Backend 

uvicorn backend.api:app --reload

---

## 🔧 Setup Instructions

### 1. Backend (FastAPI)

#### 📦 Install requirements

```bash
pip install -r requirements.txt
# Or manually:
pip install fastapi uvicorn python-multipart langchain chromadb boto3 python-dotenv

