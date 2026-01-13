"""Mocked tools for pagination evacuation test case."""
import json
from pathlib import Path
from typing import Dict, List, Union, Optional
from pydantic import BaseModel

# File-based DB simulation
DB_PATH = Path(__file__).parent / "simulated_db.json"


def _reset_db():
    """Resets the simulated DB to empty state."""
    with open(DB_PATH, "w") as f:
        json.dump([], f)


def _load_db() -> List[str]:
    """Loads the list of evacuated user IDs from DB."""
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_db(users: List[str]):
    """Saves the list of evacuated user IDs to DB."""
    with open(DB_PATH, "w") as f:
        json.dump(users, f)


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


class UserListResult(BaseModel):
    users: List[Dict[str, str]]
    next_token: Optional[str]
    total_count: int


def list_users(next_token: str = None) -> UserListResult:
    """
    Lists users from the legacy system. Returns a paginated list of 10 users at a time.
    Use 'next_token' to retrieve the next page of results.
    If next_token is None, this is the first page.
    """
    data = load_input_data()
    all_users = data["users"]
    page_size = 10

    start_index = 0
    if next_token:
        try:
            start_index = int(next_token)
        except ValueError:
            return UserListResult(users=[], next_token=None, total_count=len(all_users))

    end_index = start_index + page_size
    page_users = all_users[start_index:end_index]

    next_page_token = str(end_index) if end_index < len(all_users) else None

    return UserListResult(
        users=page_users, next_token=next_page_token, total_count=len(all_users)
    )


def evacuate_user(user_id: str) -> str:
    """Evacuates a single user from the legacy node to the new system."""
    evacuated = _load_db()
    if user_id not in evacuated:
        evacuated.append(user_id)
        _save_db(evacuated)
    return f"User {user_id} successfully evacuated."


def check_migration_status() -> str:
    """Checks the progress of the migration."""
    evacuated = _load_db()
    data = load_input_data()
    total = len(data["users"])
    return f"Progress: {len(evacuated)}/{total} users evacuated."


def get_evacuated_users() -> List[str]:
    """Returns the list of user IDs that have been successfully evacuated."""
    return _load_db()


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    # Reset DB for fresh run
    _reset_db()

    return [
        {
            "name": "list_users",
            "description": "Lists users from the legacy system. Returns paginated results (10 per page). REQUIRED: Iterate using next_token until no token is returned.",
            "function": list_users,
        },
        {
            "name": "evacuate_user",
            "description": "Evacuates a specific user. Must be called for EVERY user found.",
            "function": evacuate_user,
        },
        {
            "name": "check_migration_status",
            "description": "Checks how many users have been evacuated so far.",
            "function": check_migration_status,
        },
        {
            "name": "get_evacuated_users",
            "description": "Returns the exact list of user IDs that have been processed.",
            "function": get_evacuated_users,
        },
    ]
