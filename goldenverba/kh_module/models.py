# models.py

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GPTTopic(BaseModel):
    id: int = Field(0, alias="_id")
    intent: str = "default_intent"
    context: str = "default_context"
    examples: List[str] = []
    instructions: List[str] = []
    promptExamples: List[Optional[str]] = []
    promptId: int = -1
    test: List[Optional[str]] = []
    color: str = "unknown"

    # Added fields from Chunk
    content: str = ""
    chunk_id: int = -1
    doc_uuid: str = "unknown_uuid"
    title: str = "Untitled"
    pca: Any = None  # Replace 'Any' with the appropriate type if known
    start_i: int = 0
    end_i: int = 0
    content_without_overlap: str = ""
    labels: List[str] = []
