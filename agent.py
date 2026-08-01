import os
from typing import Literal, TypedDict
import logging

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.graph import END, StateGraph

load_dotenv()

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("devforge_agent")

class AgentState(TypedDict):
    message: str
    category: Literal["support", "unrelated"]
    reply: str

_llm_cache = None

def get_llm():
    """
    Returns ChatOllama configured for Ollama Cloud API.
    Uses singleton caching and token limits for fast responses.
    """
    global _llm_cache
    if _llm_cache is not None:
        return _llm_cache

    api_key = os.getenv("OLLAMAAPIKEY") or os.getenv("OLLAMAAPI_KEY")
    model_name = os.getenv("OLLAMA_MODEL") or os.getenv("OLLAMAMODEL") or "gemma4:cloud"

    if not api_key or api_key.strip() == "your_ollama_cloud_api_key_here":
        logger.warning("OLLAMAAPIKEY is missing or contains default placeholder.")
        raise ValueError(
            "OLLAMAAPIKEY is missing or invalid. Please configure a valid Ollama Cloud API key in your .env or Render environment variables."
        )

    logger.info(f"Connecting to Ollama Cloud with model: {model_name}")

    _llm_cache = ChatOllama(
        model=model_name,
        base_url="https://ollama.com",
        temperature=0.3,
        num_predict=220,
        client_kwargs={
            "headers": {
                "Authorization": f"Bearer {api_key}"
            }
        }
    )
    return _llm_cache

def classify_question(state: AgentState) -> AgentState:
    """
    Node 1: Checks whether the user question is related to DEVFORGE learning support or technical development.
    """
    message = state["message"].lower()

    support_words = [
        "devforge",
        "internship",
        "certificate",
        "task",
        "assignment",
        "python",
        "fastapi",
        "langchain",
        "langgraph",
        "ai",
        "web development",
        "deployment",
        "render",
        "github",
        "project",
        "learning",
        "student",
        "guide",
        "guidance",
        "code",
        "backend",
        "frontend",
        "api",
        "ollama",
        "model",
        "llm",
        "agent",
        "error",
        "bug",
        "help"
    ]

    is_related = any(word in message for word in support_words)

    category: Literal["support", "unrelated"] = "support" if is_related else "unrelated"

    logger.info(f"Classified message as: '{category}'")

    return {
        "message": state["message"],
        "category": category,
        "reply": ""
    }

def route_question(state: AgentState) -> str:
    """
    Router function to determine the next graph step.
    """
    return state["category"]

SYSTEM_PROMPT = (
    "You are DEVFORGE Student Support AI Agent.\n\n"
    "You help students with DEVFORGE internships, AI Engineering, "
    "Web Development, Python, FastAPI, LangChain, LangGraph, "
    "student projects, GitHub, Render deployment, assignments, "
    "and general technical learning guidance.\n\n"
    "FORMATTING AND STYLE RULES:\n"
    "1. Keep answers short, concise, and direct (2-4 bullet points or short paragraphs). Avoid long verbose responses.\n"
    "2. Maintain clean alignment using simple bullet dots (•) or numbers (1., 2., 3.).\n"
    "3. Absolutely DO NOT use dollar signs ($) or LaTeX math symbols in your text.\n"
    "4. Keep explanations practical, clear, friendly, and to the point.\n"
    "5. Do not invent DEVFORGE deadlines, fees, certificate policies, or internal secrets.\n"
    "6. If exact information is unavailable, politely direct the student to contact DEVFORGE support.\n"
    "7. Do not answer unrelated non-technical questions."
)

def support_agent(state: AgentState) -> AgentState:
    """
    Node 2: Sends the query to Ollama Cloud model and returns a useful, student-friendly answer.
    """
    try:
        llm = get_llm()

        response = llm.invoke([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=state["message"])
        ])

        reply_content = response.content if hasattr(response, "content") else str(response)
        reply_content = reply_content.replace("$", "")

        return {
            "message": state["message"],
            "category": "support",
            "reply": reply_content
        }
    except Exception as e:
        logger.error(f"Error calling Ollama Cloud LLM: {e}")
        return {
            "message": state["message"],
            "category": "support",
            "reply": f"⚠️ Agent Notice: Unable to connect to Ollama Cloud API. Details: {str(e)}"
        }

def unrelated_response(state: AgentState) -> AgentState:
    """
    Node 3: Safe fallback response for unrelated questions.
    """
    return {
        "message": state["message"],
        "category": "unrelated",
        "reply": (
            "I am the DEVFORGE Student Support AI Agent. "
            "I am dedicated to helping you with DEVFORGE internships, AI Engineering, "
            "Web Development, Python, FastAPI, LangChain, LangGraph, "
            "assignments, GitHub, and Render deployment guidance. "
            "Please ask a question related to these learning topics!"
        )
    }

# Build LangGraph StateGraph Workflow
workflow = StateGraph(AgentState)

# Add Nodes
workflow.add_node("classify_question", classify_question)
workflow.add_node("support_agent", support_agent)
workflow.add_node("unrelated_response", unrelated_response)

# Set Entry Point
workflow.set_entry_point("classify_question")

# Add Conditional Edges
workflow.add_conditional_edges(
    "classify_question",
    route_question,
    {
        "support": "support_agent",
        "unrelated": "unrelated_response"
    }
)

# Add Edges to END
workflow.add_edge("support_agent", END)
workflow.add_edge("unrelated_response", END)

# Compile Graph
agent_graph = workflow.compile()

def run_agent(message: str) -> dict:
    """
    Executes the LangGraph agent workflow and returns a dictionary with reply and category.
    """
    result = agent_graph.invoke({
        "message": message,
        "category": "support",
        "reply": ""
    })
    
    return {
        "reply": result["reply"],
        "category": result.get("category", "support")
    }

def stream_agent_response(message: str):
    """
    Generator function that streams response tokens in real-time.
    """
    state = classify_question({"message": message, "category": "support", "reply": ""})
    if state["category"] == "unrelated":
        yield unrelated_response(state)["reply"]
        return

    try:
        llm = get_llm()
        for chunk in llm.stream([
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content=message)
        ]):
            content = chunk.content if hasattr(chunk, "content") else str(chunk)
            if content:
                content = content.replace("$", "")
                yield content
    except Exception as e:
        logger.error(f"Streaming error: {e}")
        yield f"⚠️ Agent Notice: Unable to connect to Ollama Cloud API. Details: {str(e)}"
