# models.py (or an appropriate module)

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GPTTopic(BaseModel):
    id: int = Field(..., alias="_id")
    intent: str
    context: str
    examples: List[str]
    instructions: List[str] = []
    promptExamples: List[Optional[str]] = []
    promptId: int
    test: List[Optional[str]] = []
    color: str

    # Added fields from Chunk
    content: str
    chunk_id: int
    doc_uuid: str
    title: str
    pca: Any  # Replace 'Any' with the appropriate type if known
    start_i: int
    end_i: int
    content_without_overlap: str
    labels: List[str]
