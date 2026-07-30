# DEVFORGE Student Support AI Agent 🚀

A production-ready, cloud-hosted AI Agent designed to assist **DEVFORGE Internship** students with learning, technical coding questions, framework guidance, assignments, and deployment troubleshooting.

Built with **Python**, **FastAPI**, **LangChain**, **LangGraph**, **Ollama Cloud (Qwen Model)**, and deployed on **Render**.

---

## 🌟 Features & Highlights

- 🧠 **LangGraph Stateful Workflow**: Implements a 3-node intelligent decision workflow (`Question Classification` ➔ `Ollama Cloud Support Agent` OR `Polite Refusal Fallback`).
- ⚡ **Ollama Cloud Integration**: Powered by cloud LLM inference (`qwen3.5:cloud` or configured cloud models) via HTTPS API without needing local GPU hardware.
- 🎨 **Apple iOS Human-Designed Interface**: Embedded premium UI with Solid Off-White canvas (`#F8F9FA`), Solid Royal Purple accents (`#5B21B6`), frosted glass headers, and real-time typing feedback.
- 🛡️ **Strict Scope Safeguards**: Automatically filters out-of-scope non-technical questions to keep students focused on learning goals.
- 🚀 **One-Click Render Ready**: Includes `render.yaml` for zero-friction free cloud deployment with automatic port mapping.

---

## 🏗️ System Architecture & Workflow

```text
               +----------------------------------+
               |  Student Query via Web UI / API  |
               +----------------------------------+
                                |
                                v
                   +--------------------------+
                   |  FastAPI POST /chat      |
                   +--------------------------+
                                |
                                v
               +----------------------------------+
               | Node 1: Question Classifier      |
               | (Keyword & Domain Intent Check)  |
               +----------------------------------+
                                |
                 +--------------+--------------+
                 |                             |
       [Related / Technical]                [Unrelated]
                 |                             |
                 v                             v
  +------------------------------+  +------------------------------+
  | Node 2: Support AI Agent     |  | Node 3: Unrelated Response   |
  | (Ollama Cloud API - Qwen)    |  | (Polite Refusal Guidance)    |
  +------------------------------+  +------------------------------+
                 |                             |
                 +--------------+--------------+
                                |
                                v
                  +----------------------------+
                  |  JSON Response to Client   |
                  +----------------------------+
```

---

## 🛠️ Tech Stack

- **Backend Framework**: Python 3.10+, FastAPI, Uvicorn
- **AI Orchestration**: LangChain, LangChain-Ollama, LangGraph
- **LLM Engine**: Ollama Cloud API (`https://ollama.com` using `qwen3.5:cloud` model)
- **Frontend UI**: HTML5, CSS3 (iOS Glassmorphism, CSS Custom Properties), JavaScript (Fetch API)
- **Deployment & Hosting**: Render Web Service, GitHub

---

## 📁 Repository Structure

```text
devforge-student-support-agent/
│
├── main.py                # FastAPI server endpoints (/, /health, /chat)
├── agent.py               # LangGraph workflow nodes & Ollama Cloud LLM configuration
├── templates/
│   └── index.html         # Apple iOS-style Glassmorphism Chatbot UI
├── requirements.txt       # Production dependencies
├── .env.example           # Secret key template
├── .env                   # Local environment variables (Git-ignored)
├── .gitignore             # Git exclusion rules
├── render.yaml            # Render deployment configuration
└── README.md              # Project documentation
```

---

## 🚀 Quickstart & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/devforge-student-support-agent.git
cd devforge-student-support-agent
```

### 2. Create and Activate Virtual Environment
```bash
# Windows PowerShell
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```
Edit `.env` and insert your real **Ollama Cloud API Key**:
```env
OLLAMAAPIKEY=your_actual_ollama_cloud_api_key_here
OLLAMA_MODEL=qwen3.5:cloud
```

### 5. Run Local Server
```bash
uvicorn main:app --reload
```
Open your browser at:
- **Interactive UI**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Health Check**: [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)
- **Swagger Documentation**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🧪 Testing API Endpoints

### 1. Test Technical Query (Supported)
**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "How can I deploy my Python AI agent on Render?"}'
```
**Response:**
```json
{
  "reply": "To deploy your FastAPI AI agent on Render: 1. Push your code to GitHub with render.yaml. 2. Create a Web Service on Render. 3. Add your OLLAMAAPIKEY environment variable...",
  "category": "support",
  "agent": "DEVFORGE Student Support AI Agent"
}
```

### 2. Test Unrelated Query (Fallback Refusal)
**Request:**
```bash
curl -X POST "http://127.0.0.1:8000/chat" \
     -H "Content-Type: application/json" \
     -d '{"message": "Who will win the next cricket match?"}'
```
**Response:**
```json
{
  "reply": "I am the DEVFORGE Student Support AI Agent. I am dedicated to helping you with DEVFORGE internships, AI Engineering, Web Development, Python...",
  "category": "unrelated",
  "agent": "DEVFORGE Student Support AI Agent"
}
```

---

## ☁️ Deployment on Render

1. Push your code to your GitHub repository.
2. Sign in to [Render Dashboard](https://dashboard.render.com/).
3. Click **New +** ➔ **Web Service**.
4. Connect your GitHub repository `devforge-student-support-agent`.
5. Set the build configuration:
   - **Runtime**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
6. Under **Environment Variables**, add:
   - `OLLAMAAPIKEY`: `<your_real_ollama_api_key>`
   - `OLLAMA_MODEL`: `qwen3.5:cloud`
7. Click **Create Web Service**.

---

## 🔐 Security & Best Practices

- Real API keys are stored strictly in `.env` and Render Environment Variables.
- `.env` is explicitly listed in `.gitignore` to prevent secret leakages to public source control.
- Sample `.env.example` provides safe guidance without exposing credentials.

---

## 📜 License & Acknowledgments

Created as part of the **DEVFORGE AI Engineering Internship Program (Task 3)**.
