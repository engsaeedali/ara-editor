from typing import List, Dict, Optional
from pydantic import BaseModel

class ContextLayer(BaseModel):
    layer_type: str  # "book", "chapter", "section"
    id: str
    active_terms: List[str] = []
    tone_modifiers: Dict[str, float] = {}

class ContextTracker:
    """
    Manages the context stack to ensure consistency across the book.
    (RF-030)
    """
    def __init__(self):
        self.stack: List[ContextLayer] = []
        
    def push_context(self, layer_type: str, id: str):
        self.stack.append(ContextLayer(layer_type=layer_type, id=id))
        
    def pop_context(self):
        if self.stack:
            self.stack.pop()
            
    def get_current_context(self) -> Optional[ContextLayer]:
        return self.stack[-1] if self.stack else None
    
    def register_term_usage(self, term_id: str):
        if self.stack and term_id not in self.stack[-1].active_terms:
            self.stack[-1].active_terms.append(term_id)
                
    def get_active_terms(self) -> List[str]:
        # Collect terms from all layers
        terms = []
        for layer in self.stack:
            terms.extend(layer.active_terms)
        return list(set(terms))

context_tracker = ContextTracker()
