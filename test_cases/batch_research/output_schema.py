from pydantic import BaseModel, Field
from typing import List, Dict, Union


class BatchResearchOutput(BaseModel):
    """Output schema for batch research workflow."""

    answers: List[str] = Field(
        default_factory=list, description="Array of research answers"
    )
    citations: Union[Dict[str, str], List[str]] = Field(
        default_factory=list, description="Citations mapping or list"
    )
    synthesis: str = Field(
        default="", description="Synthesized summary of all research"
    )
