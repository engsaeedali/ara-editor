from abc import ABC, abstractmethod
from typing import Tuple, List, Dict
import logging

# Configure logging (NF-011)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("SovereignFilter")

class BaseFilter(ABC):
    """
    Abstract Base Class for all Sovereign Filters.
    Enforces the 'process' and 'correct' interface.
    """
    
    def __init__(self, name: str):
        self.name = name
        self.logger = logger
        
    @abstractmethod
    def process(self, text: str) -> Tuple[float, List[Dict]]:
        """
        Analyze text and return (score, violations).
        Score: 0.0 to 1.0 (1.0 = Perfect compliance).
        """
        pass

    @abstractmethod
    def correct(self, text: str) -> str:
        """
        Return the corrected version of the text.
        """
        pass

    def log_process(self, score: float, violations: int):
        self.logger.info(f"Filter: {self.name} | Score: {score:.2f} | Violations: {violations}")
