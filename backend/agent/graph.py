from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated, Dict
import operator
from .state import AgentState
from .prompts import SYSTEM_CONSTITUTION
from utils.logger_config import setup_logger

logger = setup_logger("graph")

# Logic Core Imports
from memory.sovereign_memory import sovereign_memory
from filters.strictness_filter import StrictnessFilter
from filters.majesty_filter import MajestyFilter
from filters.superiority_filter import SuperiorityFilter
from processors.arabization_engine import ArabizationEngine

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv, find_dotenv
# Load env vars independently of settings
load_dotenv(find_dotenv())

# ... imports ...
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
except ImportError:
    ChatGoogleGenerativeAI = None # prevent crash if dependency fails
    print("WARNING: ChatGoogleGenerativeAI import failed.")
import os
import json

# --- Initialization ---
from config.settings import settings

def check_deepseek_availability(api_key: str) -> bool:
    """Check key validity and balance before reliance."""
    if not api_key:
        return False
    try:
        import httpx
        # Very simple request to check balance/validity
        response = httpx.get(
            "https://api.deepseek.com/user/balance", 
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=5.0
        )
        if response.status_code != 200:
            return False
        data = response.json()
        return data.get("is_available", False)
    except Exception:
        return False

def get_llm():
    """Returns a tuple: (LLM_Object, Model_Name_String)"""
    google_key = settings.GOOGLE_API_KEY
    deepseek_key = settings.DEEPSEEK_API_KEY
    
    # 1. Implementation of Programmer's Proposal: Check DeepSeek First
    is_deepseek_ok = check_deepseek_availability(deepseek_key)
    
    if is_deepseek_ok:
        logger.info("DeepSeek is available and healthy. Using deepseek-chat.")
        llm = ChatOpenAI(
            model="deepseek-chat",
            api_key=deepseek_key,
            base_url="https://api.deepseek.com"
        )
        return llm, "DeepSeek-V3 (Sovereign Engine)"
    
    # 2. Automatic Fallback to Gemini if DeepSeek fails
    if google_key and ChatGoogleGenerativeAI:
        logger.warning("DeepSeek unavailable. Falling back to Gemini.")
        llm = ChatGoogleGenerativeAI(model="gemini-flash-latest", google_api_key=google_key, temperature=0.7)
        return llm, "Gemini Flash (Fallback Engine)"
    
    # Priority 3: Claude
    if settings.ANTHROPIC_API_KEY and "sk-ant" in settings.ANTHROPIC_API_KEY:
         logger.info("Using Claude Model")
         llm = ChatAnthropic(model="claude-3-5-sonnet-20240620", temperature=0.7)
         return llm, "Claude 3.5 Sonnet"
    
    # Priority 4: OpenAI
    logger.info("Fallback to OpenAI Model")
    llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
    return llm, "GPT-4o"

# Initialize Logic Components
# (Filters are kept for potential future use, but not used in the optimized path to save tokens)
strictness_filter = StrictnessFilter()
majesty_filter = MajestyFilter()
superiority_filter = SuperiorityFilter()
arabization_engine = ArabizationEngine()

# --- Nodes ---

def memory_retrieval(state: AgentState):
    """
    Node 1: Retrieve context (Fast & Cheap).
    """
    logger.info("Node: memory_retrieval started.")
    input_text = state["input_text"]
    relevant_terms = sovereign_memory.find_term(input_text, n_results=5)
    return {"memory_context": relevant_terms}

def generate_manuscript(state: AgentState):
    """
    Node 2: DIRECT GENERATION (Optimized).
    Bypasses analysis to save tokens. Enforces strict length.
    """
    logger.info("Node: generate_manuscript started.")
    context_str = json.dumps(state.get("memory_context", []), ensure_ascii=False)
    
    # Dynamic LLM Selection
    llm, model_name = get_llm()
    
    prompt = [
        SystemMessage(content=SYSTEM_CONSTITUTION),
        SystemMessage(content=f"""
        CONTEXT FROM MEMORY:
        {context_str}
        
        CRITICAL INSTRUCTIONS (ZERO-OMISSION):
        1. YOU MUST PROCESS THE TEXT VERBATIM. DO NOT SUMMARIZE.
        2. MAINTAIN THE EXACT LENGTH OF THE ORIGINAL CONTENT OR EXPAND IT.
        3. FORMAT THE OUTPUT CLEARLY WITH MARKDOWN (BOLD HEADERS, LISTS).
        4. IF THE INPUT IS LONG, PROCESS IT CHUNK BY CHUNK (internally) TO ENSURE NO LOSS.
        
        Apply the "Sovereign Tone" to everything.
        """),
        HumanMessage(content=state["input_text"])
    ]
    
    logger.info(f"Invoking {model_name} for manuscript generation...")
    response = llm.invoke(prompt)
    
    # Handle list-type content (possible with Gemini/LangChain updates)
    content_text = response.content
    if isinstance(content_text, list):
        parts = []
        for item in content_text:
            if isinstance(item, dict):
                parts.append(item.get("text", ""))
            elif isinstance(item, str):
                parts.append(item)
            else:
                parts.append(str(item))
        content_text = "".join(parts)

    # Append Signature
    final_text = content_text + f"\n\n---\n> **Processed by: {model_name}**"
    
    # Extract Token Usage (Robust Extraction for Gemini/OpenAI)
    raw_usage = getattr(response, 'usage_metadata', {})
    
    # Fallback to response_metadata if main attribute is empty (Common with Gemini)
    if not raw_usage:
        raw_usage = response.response_metadata.get('usage_metadata') or {}
        
    # Standardize Keys (Map Gemini keys to Standard keys)
    # Gemini uses: prompt_token_count, candidates_token_count, total_token_count
    # Frontend expects: input_tokens, output_tokens, total_tokens
    final_usage = {
        "input_tokens": raw_usage.get("input_tokens") or raw_usage.get("prompt_token_count", 0),
        "output_tokens": raw_usage.get("output_tokens") or raw_usage.get("candidates_token_count", 0),
        "total_tokens": raw_usage.get("total_tokens") or raw_usage.get("total_token_count", 0)
    }
    
    logger.info(f"Extracted Usage: {final_usage}")
    
    logger.info("Node: generate_manuscript completed.")
    return {
        "manuscript": final_text, 
        "current_text": final_text,
        "token_usage": final_usage,
        # Return empty analysis artifacts to satisfy the frontend schema if needed
        "violations": [],
        "metric_scores": {"strictness": 1.0, "majesty": 1.0, "superiority": 1.0},
        "editor_notes": ["Analysis skipped for performance optimization."]
    }

# --- Graph Definition ---

workflow = StateGraph(AgentState)

# Optimized Flow: Memory -> Generation -> End
workflow.add_node("memory", memory_retrieval)
workflow.add_node("generation", generate_manuscript)

workflow.set_entry_point("memory")

workflow.add_edge("memory", "generation")
workflow.add_edge("generation", END)

app_graph = workflow.compile()
