from typing import List, Dict, Tuple
from filters.base_filter import BaseFilter
import re

class SuperiorityFilter(BaseFilter):
    """
    RF-012: Superiority Filter (Positive Arrogance).
    Enforces a peer-to-peer, confident tone.
    """
    
    FORBIDDEN_TONES = [
        (r"نعتذر", "نوضح"),
        (r"عذراً", "للتوضيح"),
        (r"نأمل أن ينال إعجابكم", "نثق بأن هذا يحقق المعيار"),
        (r"إذا سمحتم", ""), # Delete completely
        (r"حاولنا قدر الإمكان", "تم إنجاز"),
    ]
    
    REQUIRED_PHRASES = [
        r"الخبرة تُثبت",
        r"المعيار",
        r"استراتيجياً",
    ]

    def __init__(self):
        super().__init__("SuperiorityFilter")

    def process(self, text: str) -> Tuple[float, List[Dict]]:
        violations = []
        score = 1.0
        
        # Check Forbidden Tones (Apologetic/Submissive)
        for weak, strong in self.FORBIDDEN_TONES:
            matches = re.finditer(weak, text)
            for match in matches:
                score -= 0.1
                violations.append({
                    "type": "submissive_tone",
                    "text": match.group(),
                    "suggestion": strong,
                    "position": match.span()
                })
        
        # Check Required Authority Markers
        found_authority = any(re.search(phrase, text) for phrase in self.REQUIRED_PHRASES)
        if not found_authority and len(text.split()) > 50: # Only penalize longer texts
            score -= 0.1
            violations.append({
                "type": "missing_authority",
                "text": "Entire Text",
                "suggestion": "Add authoritative markers like 'الخبرة تثبت'",
                "position": (0, 0)
            })
            
        return max(0.0, score), violations

    def correct(self, text: str) -> str:
        corrected_text = text
        for weak, strong in self.FORBIDDEN_TONES:
            corrected_text = re.sub(weak, strong, corrected_text)
        return corrected_text
