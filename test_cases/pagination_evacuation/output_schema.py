from pydantic import BaseModel, Field
from typing import List


class PaginationEvacuationOutput(BaseModel):
    total_users_processed: int = Field(
        description="The number of users the agent claims to have evacuated."
    )
    processed_user_ids: List[str] = Field(
        description="The exact list of user IDs that were evacuated."
    )
    final_status_message: str = Field(description="A summary message of the operation.")
    success: bool = Field(description="Whether the agent believes it finished the job.")
