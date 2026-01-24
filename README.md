# 🤖 AI-Powered Portfolio Assistant

An intelligent portfolio chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer questions about Sarah Aljudaibi's professional background, projects, skills, and experience.

![Portfolio Demo](https://img.shields.io/badge/Status-Live-success)
![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-lightgrey)
![AI](https://img.shields.io/badge/AI-Groq%20LLM-orange)

## ✨ Features

- **🧠 RAG System**: Embeds portfolio data (PDFs, JSON, Markdown) using ChromaDB vector database
- **💬 Intelligent Agent**: Understands natural language queries and retrieves relevant context
- **🎯 Smart Responses**: Powered by Groq's Llama 3.1 model for conversational, structured answers
- **🎨 Beautiful UI**: Interactive chat interface with video background
- **📊 Multi-Format Support**: Processes resumes, GitHub data, project files, and skills databases

## 🏗️ Architecture

```
User Question → RAG Retrieval → Context Extraction → LLM Reasoning → Structured Response
```

### Components:
1. **portfolio_rag.py**: Vector database system using ChromaDB and sentence-transformers
2. **portfolio_agent.py**: AI agent that orchestrates retrieval and response generation
3. **flask_app.py**: Web server handling API requests
4. **Frontend**: HTML/CSS/JS chat interface with video background

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Groq API Key ([Get one here](https://console.groq.com))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/portfolio-ai-agent.git
cd portfolio-ai-agent
```

2. **Create virtual environment**
```bash
python -m venv resumeenv
resumeenv\Scripts\activate  # Windows
# or
source resumeenv/bin/activate  # Mac/Linux
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
# Create .env file
echo GROQ_API_KEY=your_api_key_here > .env
```

5. **Run the application**
```bash
python flask_app.py
```

6. **Open in browser**
```
http://localhost:5000
```

## 💡 Example Questions

- "What projects has Sarah worked on?"
- "What are Sarah's technical skills?"
- "How many years of experience does Sarah have?"
- "Where is Sarah currently working?"
- "Tell me about Sarah's AI projects"
- "What programming languages does Sarah know?"

## 🛠️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Backend** | Flask (Python) |
| **AI Model** | Groq Llama 3.1-8B-Instant |
| **Vector DB** | ChromaDB |
| **Embeddings** | Sentence-Transformers (all-MiniLM-L6-v2) |
| **PDF Processing** | PyPDF |
| **Frontend** | HTML5, CSS3, Vanilla JavaScript |

## 📁 Project Structure

```
portfolio-ai-agent/
├── data/                      # Portfolio data files
│   ├── github data/          # GitHub profile & repos
│   ├── json/                 # Projects & skills data
│   └── *.pdf                 # Resume files
├── static/                    # Static assets
│   └── 10339-865412856.mp4   # Video background
├── templates/                 # HTML templates
│   └── index.html            # Main chat interface
├── portfolio_rag.py          # RAG system
├── portfolio_agent.py        # AI agent logic
├── flask_app.py              # Web server
├── requirements.txt          # Dependencies
└── README.md                 # This file
```

## 🤝 Contributing

This is a personal portfolio project, but feel free to fork and adapt for your own use!

## 👤 About

Created by **Sarah Aljudaibi**
- 📧 Email: sarahal.jodaiby@gmail.com
- 💼 LinkedIn: [sarah-aljudaibi](https://www.linkedin.com/in/sarah-aljudaibi/)

---

⭐ If you found this project interesting, give it a star!
