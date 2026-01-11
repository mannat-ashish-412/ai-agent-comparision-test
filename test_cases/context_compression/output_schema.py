from pydantic import BaseModel, Field
from typing import List, Union, Dict, Any


class ContextCompressionOutput(BaseModel):
    """Output schema for context compression workflow."""

    compressed_state: Union[str, Dict[str, Any]] = Field(
        default="", description="Compressed state information"
    )
    key_facts: Union[List[str], Dict[str, Any]] = Field(
        default_factory=list, description="Key facts extracted"
    )
    final_answer: str = Field(default="", description="Final compressed answer")
    sources: List[str] = Field(default_factory=list, description="Source references")
