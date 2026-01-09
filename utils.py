"""
Utility functions for the agent system.
"""

from typing import Any
from pathlib import Path
import json
from datetime import datetime

from langgraph_pydantic_agent import AgentState, Task


def save_state_to_file(state: AgentState, output_dir: str = "./outputs") -> Path:
    """
    Save agent state to a JSON file.

    Args:
        state: Agent state to save
        output_dir: Directory to save the file

    Returns:
        Path to the saved file
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"agent_state_{timestamp}.json"
    filepath = output_path / filename

    # Convert state to serializable format
    state_dict = dict(state)
    state_dict["tasks"] = [t.model_dump() for t in state.get("tasks", [])]
    state_dict["start_time"] = (
        state["start_time"].isoformat() if "start_time" in state else None
    )

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(state_dict, f, indent=2, default=str)

    return filepath


def load_state_from_file(filepath: str) -> dict:
    """
    Load agent state from a JSON file.

    Args:
        filepath: Path to the JSON file

    Returns:
        Loaded state dictionary
    """
    with open(filepath, "r", encoding="utf-8") as f:
        state_dict = json.load(f)

    # Convert tasks back to Task objects
    if "tasks" in state_dict:
        state_dict["tasks"] = [Task(**t) for t in state_dict["tasks"]]

    # Convert start_time back to datetime
    if "start_time" in state_dict and state_dict["start_time"]:
        state_dict["start_time"] = datetime.fromisoformat(state_dict["start_time"])

    return state_dict


def generate_task_graph_visualization(
    tasks: list[Task], output_file: str = "task_graph.dot"
) -> str:
    """
    Generate a DOT file for visualizing task dependencies.

    Args:
        tasks: List of tasks
        output_file: Output file path

    Returns:
        DOT file content
    """
    dot_content = ["digraph TaskGraph {"]
    dot_content.append("    rankdir=LR;")
    dot_content.append("    node [shape=box, style=rounded];")

    # Add nodes
    for task in tasks:
        color = {
            "COMPLETED": "green",
            "FAILED": "red",
            "IN_PROGRESS": "yellow",
            "PENDING": "lightblue",
            "BLOCKED": "orange",
        }.get(task.status.value, "gray")

        label = f"{task.id}\\n{task.title}"
        dot_content.append(
            f'    "{task.id}" [label="{label}", fillcolor={color}, style=filled];'
        )

    # Add edges (dependencies)
    for task in tasks:
        for dep_id in task.dependencies:
            dot_content.append(f'    "{dep_id}" -> "{task.id}";')

    dot_content.append("}")

    dot_str = "\n".join(dot_content)

    # Save to file
    with open(output_file, "w") as f:
        f.write(dot_str)

    return dot_str


def get_task_statistics(tasks: list[Task]) -> dict[str, Any]:
    """
    Get statistics about task execution.

    Args:
        tasks: List of tasks

    Returns:
        Dictionary with statistics
    """
    from collections import Counter

    status_counts = Counter(t.status.value for t in tasks)

    total_attempts = sum(t.attempt_count for t in tasks)
    avg_attempts = total_attempts / len(tasks) if tasks else 0

    return {
        "total_tasks": len(tasks),
        "completed": status_counts.get("completed", 0),
        "failed": status_counts.get("failed", 0),
        "in_progress": status_counts.get("in_progress", 0),
        "pending": status_counts.get("pending", 0),
        "blocked": status_counts.get("blocked", 0),
        "total_attempts": total_attempts,
        "average_attempts": round(avg_attempts, 2),
        "success_rate": round(status_counts.get("completed", 0) / len(tasks) * 100, 2)
        if tasks
        else 0,
    }


def validate_task_dependencies(tasks: list[Task]) -> list[str]:
    """
    Validate task dependencies and return any issues found.

    Args:
        tasks: List of tasks

    Returns:
        List of validation error messages
    """
    errors = []
    task_ids = {t.id for t in tasks}

    for task in tasks:
        # Check for missing dependencies
        for dep_id in task.dependencies:
            if dep_id not in task_ids:
                errors.append(f"Task '{task.id}' has missing dependency: '{dep_id}'")

        # Check for self-dependency
        if task.id in task.dependencies:
            errors.append(f"Task '{task.id}' has self-dependency")

    # Check for circular dependencies (simple check)
    def has_circular_dependency(task_id: str, visited: set, path: set) -> bool:
        if task_id in path:
            return True
        if task_id in visited:
            return False

        visited.add(task_id)
        path.add(task_id)

        task = next((t for t in tasks if t.id == task_id), None)
        if task:
            for dep_id in task.dependencies:
                if has_circular_dependency(dep_id, visited, path):
                    return True

        path.remove(task_id)
        return False

    visited = set()
    for task in tasks:
        if has_circular_dependency(task.id, visited, set()):
            errors.append(f"Circular dependency detected involving task '{task.id}'")

    return errors


def format_execution_summary(state: AgentState) -> str:
    """
    Format a human-readable execution summary.

    Args:
        state: Agent state

    Returns:
        Formatted summary string
    """
    tasks = state.get("tasks", [])
    stats = get_task_statistics(tasks)

    execution_time = (
        (datetime.utcnow() - state["start_time"]).total_seconds()
        if "start_time" in state
        else 0
    )

    summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                    EXECUTION SUMMARY                         ║
╚══════════════════════════════════════════════════════════════╝

📋 Request: {state.get('user_request', 'N/A')}

📊 Statistics:
   • Total Tasks: {stats['total_tasks']}
   • Completed: {stats['completed']} ✅
   • Failed: {stats['failed']} ❌
   • In Progress: {stats['in_progress']} ⏳
   • Pending: {stats['pending']} 📋
   • Success Rate: {stats['success_rate']}%
   • Average Attempts: {stats['average_attempts']}
   • Total Iterations: {state.get('iteration_count', 0)}
   • Execution Time: {execution_time:.2f}s

"""

    if state.get("error_message"):
        summary += f"❌ Error: {state['error_message']}\n"

    return summary
