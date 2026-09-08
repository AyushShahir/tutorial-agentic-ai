# 🤖 Agentic AI & RAG Tutorial Repository

Welcome to the **Agentic AI & RAG Tutorial** repository! This repository contains step-by-step implementations, hands-on tutorials, and end-to-end projects demonstrating how to build autonomous AI agents, Retrieval-Augmented Generation (RAG) systems, multimodal analysis pipelines, and memory-backed conversational tools.

> 📚 **Acknowledgment & Learning Source**:  
> The core concepts, project structures, and code tutorials in this repository were learned and adapted from the **[Codebasics YouTube Channel](https://www.youtube.com/@codebasics)** video tutorials on Agentic AI and Generative AI applications.

---

## 📁 Repository Overview

This repository is structured into progressive modules followed by production-grade mini-projects:

### ⚙️ Core Concepts & Tutorials
- `1_simple_llm_calling/` - Fundamentals of calling Large Language Models (LLMs) and structured response handling.
- `2_health_analysis/` - Domain-specific LLM application for medical/blood work analysis.
- `3_vector_db/` - Embedding creation, indexing, and vector similarity search setups.
- `4_rag_basics/` - Fundamentals of Retrieval-Augmented Generation (RAG) for querying external knowledge bases.
- `5_single_agent/` - Designing single-agent workflows equipped with external tools.
- `6_memory/` - Conversation memory patterns (short-term & long-term state management).
- `7_multimodal/` - Multimodal AI processing combining text, document analysis, and image understanding.

### 🚀 End-to-End Projects
- `Project1_Shopping_Agent/` - Autonomous shopping assistant capable of executing tools, querying product stores, checking reviews via API, and processing database transactions (`store.db`).
- `Project2_Telecom_Chatbot/` - Production RAG chatbot for telecom support using ChromaDB/vector store indexing across FAQs (`faq.csv`), PDF documents (`telecom_guide.pdf`), and ticket management (`tickets.db`).

---

## 🛠️ Prerequisites & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/AyushShahir/tutorial-agentic-ai.git
cd tutorial-agentic-ai
```

### 2. Install Dependencies using `uv`
This project utilizes [`uv`](https://github.com/astral-sh/uv) for fast package management.

```bash
uv sync
```

*(Alternatively, standard python virtual environments can be used with `pip`)*

### 3. Environment Variables setup
Create a `.env` file in the root directory (or project folders) based on required API keys:

```env
GROQ_API_KEY=your_groq_api_key_here
GOOGLE_API_KEY=your_google_api_key_here
```

---

## 🧪 Running the Code

- **Notebooks**: Open any `.ipynb` file inside the step directories (`1_simple_llm_calling`, `7_multimodal`, etc.) using Jupyter or VS Code.
- **Projects**: Navigate to project folders (e.g., `Project2_Telecom_Chatbot`) and execute the main entrypoint:
  ```bash
  python Project2_Telecom_Chatbot/main.py
  ```

---

## 🙏 Credits & Acknowledgments

Special thanks to **Codebasics** for their outstanding educational content on Data Science, AI, and Agentic AI engineering.
