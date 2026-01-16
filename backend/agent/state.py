from typing import TypedDict, List, Optional, Dict

class AgentState(TypedDict):
    input_text: str
    current_text: str
    manuscript: str  # The final clean text
    editor_notes: List[str]  # List of notes from the editor
    
    # Logic Core (Phase 2 Additions)
    memory_context: List[Dict] # Retrieved terms/concepts from SovereignMemory
    violations: List[Dict] # Collected violations from filters
    metric_scores: Dict[str, float] # Scores from filters (Strictness, Majesty, Superiority)
    token_usage: Optional[Dict] # Token usage statistics
    
    revision_count: int
    status: str
