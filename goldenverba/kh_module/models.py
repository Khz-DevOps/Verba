# models.py

from pydantic import BaseModel, Field
from typing import List, Optional, Any

class GPTTopic(BaseModel):
    id: Optional[int] = Field(None, alias="_id")
    intent: Optional[str] = None
    context: Optional[str] = None
    examples: Optional[List[str]] = []
    instructions: Optional[List[str]] = []
    promptExamples: Optional[List[Optional[str]]] = []
    promptId: Optional[int] = None
    test: Optional[List[Optional[str]]] = []
    color: Optional[str] = None

    # Added fields from Chunk
    content: Optional[str] = None
    chunk_id: Optional[int] = None
    doc_uuid: Optional[str] = None  # Made Optional
    title: Optional[str] = None
    pca: Optional[Any] = None  # Replace 'Any' with the appropriate type if known
    start_i: Optional[int] = None
    end_i: Optional[int] = None
    content_without_overlap: Optional[str] = None
    labels: Optional[List[str]] = []
