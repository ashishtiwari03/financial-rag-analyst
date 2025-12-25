
# 💰 Financial Report Analyst (Multimodal RAG)

A sophisticated AI Agent that analyzes complex financial documents (PDFs) and answers questions with high accuracy. Unlike standard RAG tools, this project specializes in reading **tables** and structured data from Annual Reports and 10-Ks using LlamaParse and Vector Search.

## 🚀 Features
* **Table-Aware Parsing:** Accurately extracts data from rows/columns in PDFs (solves the "mashed text" problem).
* **Hybrid Architecture:**
    * **Privacy-First:** Uses local embeddings (Ollama) to keep vector data on your machine.
    * **High Speed:** Uses Groq (Llama 3.1) for instant reasoning and answers.
* **Citations:** Retrieves the exact page and context for every answer.
* **Zero Cost:** Built entirely using free tiers and open-source models.

## 🛠️ Tech Stack
* **Orchestration:** [LlamaIndex](https://www.llamaindex.ai/)
* **Parser:** [LlamaParse](https://cloud.llamaindex.ai/) (Markdown-based PDF parsing)
* **Database:** [ChromaDB](https://www.trychroma.com/) (Local Vector Store)
* **LLM (Reasoning):** [Groq](https://groq.com/) (Llama 3.1 8B)
* **Embeddings:** [Ollama](https://ollama.com/) (nomic-embed-text)
* **UI:** [Streamlit](https://streamlit.io/)

---

## ⚙️ Prerequisites
Before running the app, ensure you have the following installed:

1.  **Python 3.10+**
2.  **Ollama** (for local embeddings)
    * Download from [ollama.com](https://ollama.com)
    * Run this command in your terminal to pull the embedding model:
        ```bash
        ollama pull nomic-embed-text
        ```

---

## 📦 Installation Guide

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/yourusername/finance-rag.git](https://github.com/yourusername/finance-rag.git)
    cd finance-rag
    ```

2.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    
    # Windows:
    .\venv\Scripts\activate
    # Mac/Linux:
    source venv/bin/activate
    ```

3.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🔑 Configuration (.env)
This project uses a `.env` file to manage API keys securely.

1.  Create a file named `.env` in the root directory.
2.  Add your API keys (Get them from [LlamaCloud](https://cloud.llamaindex.ai/) and [Groq Console](https://console.groq.com/)):

    ```ini
    LLAMA_CLOUD_API_KEY=llx-your-key-here
    GROQ_API_KEY=gsk-your-key-here
    ```

---

## ▶️ Usage

1.  **Start the Application**
    ```bash
    streamlit run app.py
    ```

2.  **Using the App:**
    * Open your browser (usually `http://localhost:8501`).
    * Upload a Financial PDF (e.g., an Annual Report or 10-K).
    * Click **"Process File"**.
    * Ask questions like: *"What is the forecasted revenue for Q4?"* or *"Summarize the risks table."*

---

## 📂 Project Structure
```text
├── .env               # API Keys (Not uploaded to GitHub)
├── .gitignore         # Files to ignore (venv, secrets)
├── app.py             # The Streamlit Frontend
├── rag_engine.py      # The RAG Logic (LlamaIndex + Groq)
├── requirements.txt   # List of Python libraries
└── chroma_db/         # Local Vector Database storage
