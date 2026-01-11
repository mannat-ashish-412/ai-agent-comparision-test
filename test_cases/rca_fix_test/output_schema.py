from pydantic import BaseModel, Field
from typing import List, Union


class RcaFixTestOutput(BaseModel):
    """Output schema for RCA fix test workflow."""

    root_cause: str = Field(
        default="", description="Identified root cause of the issue"
    )
    proposed_patch: str = Field(default="", description="Code patch to fix the issue")
    regression_tests: List[str] = Field(
        default_factory=list, description="Test cases to prevent regression"
    )
    test_explanations: Union[str, List[str]] = Field(
        default="", description="Explanations for the test cases"
    )
