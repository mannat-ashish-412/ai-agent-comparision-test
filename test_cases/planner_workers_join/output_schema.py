from pydantic import BaseModel, Field
from typing import Dict, Any


class ConsistencyCheck(BaseModel):
    """Results of technical consistency validation."""

    is_consistent: bool = Field(
        default=True,
        description="Whether the technical recommendations are consistent.",
    )
    notes: str = Field(
        default="", description="Summary of the consistency validation findings."
    )


class DatabaseMigrationPlan(BaseModel):
    """Unified architectural plan for database migration."""

    unified_plan: str = Field(
        default="", description="The complete, cohesive technical migration document."
    )
    findings_by_area: Dict[str, Any] = Field(
        default_factory=dict,
        description="Detailed technical findings grouped by focus area.",
    )
    consistency_check: ConsistencyCheck = Field(
        default_factory=lambda: ConsistencyCheck(),
        description="Validation results ensuring all sections are compatible.",
    )
