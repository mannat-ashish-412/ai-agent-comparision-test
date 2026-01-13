from pydantic import BaseModel, Field
from typing import Dict


class DependencyUpdateOutput(BaseModel):
    """The result of the dependency update task."""

    final_packages: Dict[str, str] = Field(
        default_factory=dict,
        description="Dictionary of installed packages and their versions after update.",
    )
    success: bool = Field(
        ...,
        description="True if the goal (updating requests) was achieved without test failures.",
    )
    description: str = Field(
        default="", description="Explanation of the actions taken."
    )
