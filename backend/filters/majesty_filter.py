from typing import List, Dict, Tuple
from filters.base_filter import BaseFilter
from config.settings import settings

class MajestyFilter(BaseFilter):
    """
    RF-011: Majesty and Solemnity Filter.
    Enforces high lexical density and sovereign tone.
    """
    
    # Dictionary of Majestic Terms (Simple version for Phase 2)
    # In a full production system, this would load from a larger database or JSON file.
    MAJESTIC_TERMS = {
        "جليل", "رفيع", "سام", "عظيم", "مهيب",
        "وقور", "رصين", "متين", "جزيل", "سيادي",
        "محوري", "استراتيجي", "جوهري", "حاسم"
    }
    
    WEAK_TERMS_REPLACEMENT = {
        "جيد": "متين",
        "كبير": "هائل",
        "مهم": "محوري",
        "جميل": "بديع",
        "قوي": "راسخ",
        "سريع": "خاطف"
    }

    def __init__(self):
        super().__init__("MajestyFilter")

    def process(self, text: str) -> Tuple[float, List[Dict]]:
        violations = []
        words = text.split()
        total_words = len(words)
        if total_words == 0:
            return 1.0, []

        majestic_count = sum(1 for w in words if w in self.MAJESTIC_TERMS)
        density = majestic_count / total_words

        # Threshold from Settings (Default 0.3)
        threshold = settings.MAJESTY_THRESHOLD
        
        score = min(1.0, density / threshold) # 1.0 if density >= threshold
        
        # Check for weak words
        for i, word in enumerate(words):
            if word in self.WEAK_TERMS_REPLACEMENT:
                 violations.append({
                    "type": "weak_lexicon",
                    "text": word,
                    "suggestion": self.WEAK_TERMS_REPLACEMENT[word],
                    "position": (i, i+1) # Approximate
                })
        
        return score, violations

    def correct(self, text: str) -> str:
        words = text.split()
        corrected_words = []
        for word in words:
            if word in self.WEAK_TERMS_REPLACEMENT:
                corrected_words.append(self.WEAK_TERMS_REPLACEMENT[word])
            else:
                corrected_words.append(word)
        return " ".join(corrected_words)
