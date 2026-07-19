# Multi-Agent Customer Support Chatbot (RAG)

An AI-powered customer support chatbot that uses **Retrieval-Augmented Generation (RAG)**, **LangChain**, and specialized AI agents to answer customer queries related to products, billing, refunds, shipping, technical support, complaints, and FAQs. The application features a modern React frontend, FastAPI backend, vector search with ChromaDB, and conversation memory stored in MongoDB.

---

# Features

* Multi-Agent Architecture
* Intent Detection
* Retrieval-Augmented Generation (RAG)
* ChromaDB Vector Database
* MongoDB Conversation Memory
* PDF Knowledge Base
* React + Vite Frontend
* FastAPI Backend
* Modern Chat Interface
* Semantic Search using Sentence Transformers

---

# Technology Stack

## Backend

* Python 3.10+
* FastAPI
* LangChain
* ChromaDB
* Sentence Transformers (all-MiniLM-L6-v2)
* MongoDB Atlas
* PyMongo
* Uvicorn

## Frontend

* React
* Vite
* Node.js
* JavaScript
* CSS

## AI & RAG

* Groq LLM
* LangChain
* Retrieval-Augmented Generation (RAG)
* ChromaDB
* PDF Knowledge Base

---

# Project Structure

```text
.
├── backend/
│   ├── agents/
│   ├── history/
│   ├── rag/
│   └── vectorstore/
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
├── knowledge_base/
├── app.py
├── requirements.txt
├── package.json
└── README.md
```

---

# Prerequisites

Install the following before running the project:

* Python 3.10 or later
* Node.js (includes npm)
* Git
* MongoDB Atlas account
* Groq API Key

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/shobhit-jpg/MultiAgent-Customer-chatbot-RAG.git
cd MultiAgent-Customer-chatbot-RAG
```

---

## 2. Create a Python virtual environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

## 3. Install Python dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Install frontend dependencies

Move into the frontend folder:

```bash
cd frontend
```

Install Node packages:

```bash
npm install
```

Return to the project root:

```bash
cd ..
```

---

## 5. Configure Environment Variables

Create a `.env` file in the project root.

Example:

```env
GROQ_API_KEY=your_groq_api_key
MONGODB_URI=your_mongodb_connection_string
DATABASE_NAME=customer_support
```

---
--

# Running the Application

## Start the Backend

```bash
python app.py
```

or

```bash
uvicorn app:app --reload
```

---

## Start the Frontend

Open another terminal.

```bash
cd frontend
npm run dev
```

Vite will provide a local URL (typically `http://localhost:5173`).

---

# How the Chatbot Works

1. User submits a query.
2. Intent Detector identifies the query category.
3. Router forwards the request to the appropriate specialized agent.
4. Relevant documents are retrieved from ChromaDB.
5. The LLM generates a context-aware response.
6. Conversation history is stored in MongoDB for future interactions.

---

# Supported Customer Support Domains

* Billing
* Products
* Technical Support
* Shipping
* Refund Policy
* Warranty
* Complaints
* Frequently Asked Questions

---

# Future Improvements

* Authentication
* Streaming Responses
* Voice Support
* Admin Dashboard
* Analytics
* Multi-language Support
* Docker Deployment
* Cloud Deployment

---

# License

This project is intended for educational and portfolio purposes.
