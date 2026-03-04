from pydantic import BaseModel, Field
from typing import List


class AppSecurityOutput(BaseModel):
    """The final answer from the application security engineer."""

    code: str = Field(..., description="The fixed, secure code snippet.")
    verification_status: bool = Field(
        ..., description="True if the code passed all security verification checks."
    )
    vulnerability_check_result: str = Field(
        default="UNKNOWN",
        description="The final result from the verify_security tool (e.g., SAFE, VULNERABLE).",
    )
    verification_payloads_tested: List[str] = Field(
        default_factory=list,
        description="List of payload types used during verification (e.g., ['standard', 'polyglot']).",
    )
