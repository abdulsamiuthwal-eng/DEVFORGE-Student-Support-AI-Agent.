import os
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent import run_agent

app = FastAPI(
    title="DEVFORGE Student Support AI Agent",
    description="An AI agent built with LangChain, LangGraph, FastAPI, and Ollama Cloud.",
    version="1.0.0"
)

# Enable CORS for frontend/API flexibility
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Jinja2 Templates directory
templates_dir = os.path.join(os.path.dirname(__file__), "templates")
templates = Jinja2Templates(directory=templates_dir)

class ChatRequest(BaseModel):
    message: str = Field(..., example="How can I deploy my Python AI agent on Render?")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    """
    Renders the Apple iOS-inspired Glassmorphism Chatbot UI.
    Also returns JSON if Accept header explicitly demands JSON.
    """
    accept_header = request.headers.get("accept", "")
    if "text/html" not in accept_header and "application/json" in accept_header:
        return {
            "message": "Welcome to DEVFORGE Student Support AI Agent",
            "documentation": "/docs"
        }
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api-info")
def api_info():
    """
    Returns API metadata and documentation path.
    """
    return {
        "message": "Welcome to DEVFORGE Student Support AI Agent",
        "documentation": "/docs"
    }

@app.get("/health")
def health():
    """
    Returns the application health status.
    """
    return {
        "status": "healthy",
        "service": "DEVFORGE Student Support AI Agent"
    }

@app.post("/chat")
def chat(request: ChatRequest):
    """
    Processes student messages through the LangGraph AI workflow.
    """
    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty."
        )

    try:
        result = run_agent(request.message.strip())

        return {
            "reply": result["reply"],
            "category": result.get("category", "support"),
            "agent": "DEVFORGE Student Support AI Agent"
        }

    except ValueError as val_err:
        raise HTTPException(
            status_code=400,
            detail=str(val_err)
        )
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution error: {str(error)}"
        )
