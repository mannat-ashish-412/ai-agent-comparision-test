"""
Exception classes for the agent system.
"""


class AgentSystemError(Exception):
    """Base exception for agent system errors."""

    pass


class ConfigurationError(AgentSystemError):
    """Raised when there's a configuration error."""

    pass


class TaskExecutionError(AgentSystemError):
    """Raised when task execution fails."""

    def __init__(self, task_id: str, message: str):
        self.task_id = task_id
        super().__init__(f"Task {task_id} failed: {message}")


class VerificationError(AgentSystemError):
    """Raised when task verification fails."""

    def __init__(self, task_id: str, message: str):
        self.task_id = task_id
        super().__init__(f"Verification failed for task {task_id}: {message}")


class MaxRetriesExceededError(AgentSystemError):
    """Raised when max retry attempts are exceeded."""

    def __init__(self, task_id: str, max_attempts: int):
        self.task_id = task_id
        self.max_attempts = max_attempts
        super().__init__(f"Task {task_id} failed after {max_attempts} attempts")


class MaxIterationsExceededError(AgentSystemError):
    """Raised when max workflow iterations are exceeded."""

    def __init__(self, max_iterations: int):
        self.max_iterations = max_iterations
        super().__init__(f"Workflow exceeded max iterations: {max_iterations}")


class DependencyError(AgentSystemError):
    """Raised when there's a task dependency issue."""

    def __init__(self, task_id: str, dependency_id: str):
        self.task_id = task_id
        self.dependency_id = dependency_id
        super().__init__(f"Task {task_id} has unmet dependency: {dependency_id}")
