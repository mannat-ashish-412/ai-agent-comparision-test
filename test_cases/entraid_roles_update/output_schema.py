from pydantic import BaseModel, Field
from typing import List


class EntraIDUpdateOutput(BaseModel):
    processed_users: List[str] = Field(
        description="List of user IDs that were processed."
    )
    final_status: str = Field(description="A summary of the update process.")
    all_requests_verified: bool = Field(
        description="True if all update requests were successfully verified."
    )
