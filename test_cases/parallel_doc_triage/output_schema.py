from pydantic import BaseModel, Field
from typing import List, Literal


class DuplicateMerge(BaseModel):
    """Details regarding issues identified as duplicates and merged into a primary record."""

    primary: str = Field(default="", description="The ID of the main issue record.")
    duplicates: List[str] = Field(
        default_factory=list,
        description="List of IDs that were identified as duplicates.",
    )
    reason: str = Field(
        default="",
        description="The explanation of why these issues were determined to be duplicates.",
    )


class ProcessedItem(BaseModel):
    """The final state of an individual unique issue after classification and analysis."""

    id: str = Field(default="", description="The unique identifier for the issue.")
    classification: Literal["bug", "feature", "question"] = Field(
        default="bug", description="The category assigned to the issue."
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(
        default="low", description="The priority level."
    )
    next_action: str = Field(default="", description="The recommended next step.")


class WorkflowOutput(BaseModel):
    """The final structured output schema for the issue triage workflow."""

    processed_items: List[ProcessedItem] = Field(
        default_factory=list, description="List of all unique issues after processing."
    )
    duplicates_merged: List[DuplicateMerge] = Field(
        default_factory=list,
        description="Records of which issues were identified as duplicates.",
    )
