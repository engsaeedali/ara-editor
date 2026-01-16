import re
from typing import List, Dict, Tuple
from filters.base_filter import BaseFilter

class StrictnessFilter(BaseFilter):
    """
    RF-010: Strictness and Brutal Honesty Filter.
    Uses Regex to detect weak language.
    """
    
    FORBIDDEN_PATTERNS = [
        (r"يمكن تحسين", "يجب إصلاح"),
        (r"نقترح مراجعة", "يتوجب إعادة هندسة"),
        (r"من المفضل", "من الضروري"),
        (r"بإمكاننا", "علينا"),
        (r"ربما", "بالتأكيد"),
        (r"يحتمل", "من المؤكد"),
        (r"قد يكون", "هو"),
        (r"نرى أن", "الواقع يفرض"),
    ]
    
    def __init__(self):
        super().__init__("StrictnessFilter")

    def process(self, text: str) -> Tuple[float, List[Dict]]:
        violations = []
        score = 1.0
        
        for weak, strong in self.FORBIDDEN_PATTERNS:
            matches = re.finditer(weak, text)
            for match in matches:
                score -= 0.05 # Deduct points for each violation
                violations.append({
                    "type": "weak_language",
                    "text": match.group(),
                    "suggestion": strong,
                    "position": match.span()
                })
        
        # Ensure score is between 0 and 1
        return max(0.0, score), violations

    def correct(self, text: str) -> str:
        """
        Auto-correction mechanism (Deterministic)
        """
        corrected_text = text
        for weak, strong in self.FORBIDDEN_PATTERNS:
            corrected_text = re.sub(weak, strong, corrected_text)
        return corrected_text
