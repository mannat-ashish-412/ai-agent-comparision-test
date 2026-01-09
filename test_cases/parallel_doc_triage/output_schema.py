from pydantic import BaseModel, Field
from typing import List, Dict, Literal


class DuplicateMerge(BaseModel):
    """Details regarding issues identified as duplicates and merged into a primary record."""

    primary: str = Field(description="The ID of the main issue record.")
    duplicates: List[str] = Field(
        description="List of IDs that were identified as duplicates of the primary."
    )
    reason: str = Field(
        description="The logical justification for merging these specific items."
    )


class ProcessedItem(BaseModel):
    """The final state of an individual unique issue after classification and analysis."""

    id: str = Field(
        description="The unique identifier for the issue (e.g., ISSUE-001)."
    )
    classification: Literal["bugs", "features", "questions"] = Field(
        description="The category the item was assigned to."
    )
    severity: Literal["critical", "high", "medium", "low"] = Field(
        description="The priority level based on impact."
    )
    next_action: str = Field(
        description="The immediate next step required for this item."
    )
    processed_by_agent: bool = Field(
        description="Whether this item was handled by the AI agent."
    )


class AgentTrace(BaseModel):
    """Metadata regarding the agent's execution path and reasoning steps."""

    steps: List[str] = Field(
        description="A list of internal steps the agent took to reach the conclusion."
    )
    confidence_score: float = Field(
        description="The agent's confidence in the final classification (0.0 to 1.0)."
    )


class WorkflowOutput(BaseModel):
    """The final structured output schema for the long-running workflow."""

    processed_items: List[ProcessedItem] = Field(
        description="List of all unique items after processing and validation."
    )
    duplicates_merged: List[DuplicateMerge] = Field(
        description="Records of which items were consolidated into primary entries."
    )
    agent_trace: AgentTrace = Field(
        description="Detailed trace of the agent's logic during the workflow."
    )
