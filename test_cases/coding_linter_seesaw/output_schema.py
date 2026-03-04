from pydantic import BaseModel, Field


class RefactoredCodeOutput(BaseModel):
    """The result of the refactoring task."""

    refactored_code: str = Field(
        ..., description="The final code content after attempts to fix linter errors."
    )
    strategy_used: str = Field(
        default="unknown",
        description="The strategy used to resolve conflicts (e.g., 'standard_fix', 'disable_lint_rule', 'human_help').",
    )
    resolution_successful: bool = Field(
        ..., description="True if the conflict was resolved/passed, False if stuck."
    )
    loop_detected: bool = Field(
        default=False,
        description="Did the agent detect that it was in an infinite loop?",
    )
