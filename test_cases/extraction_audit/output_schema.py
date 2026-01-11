from pydantic import BaseModel, Field
from typing import List, Dict, Any


class Contradiction(BaseModel):
    """Detailed information about a technical contradiction found between requirements."""

    category: str = Field(
        default="", description="The functional category where the conflict was found."
    )
    items: List[str] = Field(
        default_factory=list,
        description="The specific requirement strings that are in conflict.",
    )
    severity: str = Field(default="low", description="The assessed business impact.")
    reason: str = Field(
        default="", description="Logical explanation of the contradiction."
    )


class ExtractionAuditOutput(BaseModel):
    """The final structured audit report for the requirement extraction and analysis process."""

    prd: Dict[str, Any] = Field(
        default_factory=dict,
        description="Structured product requirements document organized by category.",
    )
    contradictions: List[Contradiction] = Field(
        default_factory=list,
        description="List of all unique technical contradictions identified.",
    )
    clarifying_questions: List[str] = Field(
        default_factory=list,
        description="Suggested questions for stakeholders to resolve conflicts.",
    )
