from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime
from enum import Enum

# --- User & Project Models (ER-001) ---

class UserRole(str, Enum):
    AUTHOR = "author"
    EDITOR = "editor"
    ADMIN = "admin"

class User(BaseModel):
    id: str = Field(..., description="Unique User ID")
    email: str = Field(..., description="Email Address")
    name: str = Field(..., description="Full Name")
    role: UserRole = Field(default=UserRole.AUTHOR)
    created_at: datetime = Field(default_factory=datetime.now)
    settings: Dict = Field(default_factory=dict)

class BookProject(BaseModel):
    id: str = Field(..., description="Project ID")
    title: str = Field(..., description="Book Title")
    author_id: str = Field(..., description="Author ID")
    field: str = Field(..., description="Knowledge Field")
    specialization: str = Field(..., description="Precise Specialization")
    mission: str = Field(..., description="Central Mission")
    target_audience: List[str] = Field(..., description="Target Audience")
    tone_profile: Dict = Field(..., description="Tone Profile")
    status: str = Field(default="active")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

# --- Chapter & Memory Models (ER-002) ---

class ArabicTerm(BaseModel):
    id: str = Field(..., description="Term ID")
    english_term: str = Field(..., description="English Term")
    arabic_translation: str = Field(..., description="Arabic Translation")
    arabic_root: Optional[str] = Field(None, description="Arabic Root")
    definition: Optional[str] = Field(None, description="Definition")
    source: str = Field(..., description="Source (Memory, Academic, Heritage, Creative)")
    confidence: float = Field(default=1.0, description="Confidence Score")
    first_used_in: Optional[str] = Field(None, description="First Chapter Used In")
    usage_count: int = Field(default=0)
    alternatives: List[str] = Field(default_factory=list)

class Chapter(BaseModel):
    id: str = Field(..., description="Chapter ID")
    book_id: str = Field(..., description="Book ID")
    title: str = Field(..., description="Chapter Title")
    chapter_number: int = Field(..., description="Chapter Number")
    
    # Content
    raw_content: str = Field(..., description="Raw Input Content")
    processed_content: Optional[str] = Field(None, description="Processed Sovereign Content")
    
    # Analysis & Memory
    arabic_terms: List[ArabicTerm] = Field(default_factory=list, description="Arabic Terms Used")
    key_concepts: List[str] = Field(default_factory=list, description="Key Concepts")
    historical_references: List[Dict] = Field(default_factory=list, description="Historical References")
    structural_pattern: Optional[str] = Field(None, description="Structural Pattern Used")
    
    # Metadata
    processing_metrics: Optional[Dict] = Field(None, description="Quality Scale Metrics")
    approval_status: str = Field(default="pending")
    created_at: datetime = Field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
