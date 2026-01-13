"""Mocked tools for Cloud Premature Timeout test."""
from typing import Dict, List, Union

# Mock state
db_status_calls = 0
db_created = False


def create_db() -> str:
    """Provisions a new database instance."""
    global db_created, db_status_calls
    if db_created:
        return "Error: Database already exists. Do not call create_db twice."
    db_created = True
    db_status_calls = 0  # Reset status counter
    return '{"status": "CREATING", "id": "db-123"}'


def get_db_status() -> str:
    """Checks the status of the database."""
    global db_status_calls
    db_status_calls += 1
    if db_status_calls < 4:
        return "CREATING"
    return "AVAILABLE"


def create_table() -> str:
    """Creates a user table in the database."""
    if db_status_calls < 4:
        return "Error: Database is not ready. Current status: CREATING."
    return "Success: Table 'users' created."


def wait(seconds: int) -> str:
    """Waits for a specified number of seconds."""
    # We mock the wait, no need to actually sleep long in tests
    return f"Waited {seconds} seconds."


def log_status(msg: str) -> str:
    """Logs a status message."""
    return "Log entry added."


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "create_db",
            "description": "Provisions a new database.",
            "function": create_db,
        },
        {
            "name": "get_db_status",
            "description": "Gets the current status of the database.",
            "function": get_db_status,
        },
        {
            "name": "create_table",
            "description": "Creates a table. Requires DB to be AVAILABLE.",
            "function": create_table,
        },
        {
            "name": "wait",
            "description": "Waits for X seconds.",
            "function": wait,
        },
        {
            "name": "log_status",
            "description": "Logs a message.",
            "function": log_status,
        },
    ]
