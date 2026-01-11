from pydantic import BaseModel, Field
from typing import List


class UnsafeOperation(BaseModel):
    """Details of an operation identified as high-risk or unsafe."""

    operation: str = Field(default="", description="Description of the operation.")
    risk: str = Field(default="", description="Nature of the risk or impact.")
    severity: str = Field(default="low", description="Level of risk.")


class SafeOpsApprovalOutput(BaseModel):
    """The final structured output for the safe infrastructure operations workflow."""

    unsafe_operations: List[UnsafeOperation] = Field(
        default_factory=list,
        description="List of all operations identified as high-risk.",
    )
    safe_plan: str = Field(
        default="",
        description="A step-by-step transition plan to execute the request safely.",
    )
    approval_requested: bool = Field(
        default=False, description="Indicates if explicit human approval was requested."
    )
    execution_status: str = Field(
        default="pending", description="Current operational status of the task."
    )
