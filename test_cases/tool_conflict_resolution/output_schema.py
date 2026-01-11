from pydantic import BaseModel, Field
from typing import List


class DetectedConflict(BaseModel):
    """Detailed report of a data discrepancy found between multiple systems."""

    systems: List[str] = Field(
        default_factory=list,
        description="Names of the systems reporting conflicting data.",
    )
    prices: List[float] = Field(
        default_factory=list,
        description="The actual conflicting price values reported.",
    )
    discrepancy: float = Field(
        default=0.0, description="The absolute difference between the reported values."
    )


class ToolConflictResolutionOutput(BaseModel):
    """The final structured integrity report for the data consistency and arbitration process."""

    detected_conflicts: List[DetectedConflict] = Field(
        default_factory=list, description="List of all data discrepancies identified."
    )
    resolution_policy: str = Field(
        default="",
        description="The selected arbitration policy used to resolve the conflict.",
    )
    final_price: float = Field(
        default=0.0,
        description="The final verified price determined after system arbitration.",
    )
    audit_trail: str = Field(
        default="", description="A formal audit note explaining the justification."
    )
