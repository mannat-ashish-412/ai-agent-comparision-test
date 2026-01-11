from typing import List, Optional, Literal, Dict, Any
from pydantic import BaseModel, Field


class Task(BaseModel):
    id: str
    description: str
    dependencies: List[str] = Field(default_factory=list)
    status: Literal["pending", "in_progress", "completed", "failed"] = "pending"
    result_summary: Optional[str] = None
    retry_count: int = 0
    feedback_log: List[str] = Field(default_factory=list)


class WorkflowState(BaseModel):
    user_goal: str
    plan: List[Task] = Field(default_factory=list)
    current_task_id: Optional[str] = None
    global_context: Dict[str, Any] = Field(default_factory=dict)
    max_retries: int = 3
