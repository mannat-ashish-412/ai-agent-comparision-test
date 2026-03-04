"""Mocked tools for entraid roles update test case."""
import json
import uuid
import time
import random
from pathlib import Path
from typing import Dict, List, Union

import threading

# File-based DB simulation
DB_PATH = Path(__file__).parent / "simulated_db.json"
REQUESTS_PATH = Path(__file__).parent / "simulated_requests.json"
RATE_LIMIT_PATH = Path(__file__).parent / "rate_limit.json"

_db_lock = threading.Lock()
_last_update_time = 0
_update_count = 0


def _reset_db():
    """Resets the simulated DB and requests to empty state."""
    global _last_update_time, _update_count
    with _db_lock:
        with open(DB_PATH, "w") as f:
            json.dump([], f)
        with open(REQUESTS_PATH, "w") as f:
            json.dump({}, f)
        with open(RATE_LIMIT_PATH, "w") as f:
            json.dump({"last_reset": time.time(), "count": 0}, f)
        _last_update_time = 0
        _update_count = 0


def _load_db() -> List[Dict]:
    """Loads the state of users from DB."""
    if not DB_PATH.exists():
        return []
    with open(DB_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def _save_db(data: List[Dict]):
    """Saves the state of users to DB."""
    with open(DB_PATH, "w") as f:
        json.dump(data, f)


def _load_requests() -> Dict:
    """Loads request statuses."""
    if not REQUESTS_PATH.exists():
        return {}
    with open(REQUESTS_PATH, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def _save_requests(data: Dict):
    """Saves request statuses."""
    with open(REQUESTS_PATH, "w") as f:
        json.dump(data, f)


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def list_entraid_users() -> List[Dict[str, str]]:
    """
    Lists all users currently in EntraID.
    Returns a list of dictionaries containing 'id', 'name', and 'current_roles'.
    """
    data = load_input_data()
    return data["users"]


def get_role_instructions() -> str:
    """
    Retrieves the unstructured text containing role assignment instructions from HR/IT.
    """
    data = load_input_data()
    return data["role_instructions"]


def update_user_roles(user_id: str, new_roles: List[str]) -> str:
    """
    Updates the roles for a specific user.
    Returns a Request ID (UUID string) that MUST be verified later.

    RATE LIMITED: Max 3 updates per second. Will return error if exceeded.
    """
    global _last_update_time, _update_count

    current_time = time.time()

    with _db_lock:
        # Rate limiting logic
        if current_time - _last_update_time < 1.0:
            _update_count += 1
            if _update_count > 3:
                return f"ERROR: Rate limit exceeded. Max 3 updates per second. Wait {1.0 - (current_time - _last_update_time):.2f}s"
        else:
            _last_update_time = current_time
            _update_count = 1

        request_id = str(uuid.uuid4())

        # 1. Update Requests Log
        requests = _load_requests()
        requests[request_id] = {
            "user_id": user_id,
            "roles": new_roles,
            "status": "Pending",
            "retry_count": 0,
            "created_at": current_time,
        }
        _save_requests(requests)

        # 2. Update Actual DB (Simulating the effect)
        current_db = _load_db()
        user_found = False
        for u in current_db:
            if u["id"] == user_id:
                u["assigned_roles"] = new_roles
                user_found = True
                break
        if not user_found:
            current_db.append({"id": user_id, "assigned_roles": new_roles})

        _save_db(current_db)

    return request_id


def verify_request_status(request_id: str) -> str:
    """
    Checks the status of a role update request.
    Returns "Success", "Failed", or "Pending".

    IMPORTANT: First verification attempt has 40% chance of failure.
    Retry on same request_id will succeed.
    """
    with _db_lock:
        requests = _load_requests()
        if request_id not in requests:
            return "Error: Request ID not found."

        req_data = requests[request_id]

        # If already successful, return success
        if req_data["status"] == "Success":
            return f"Request {request_id} Status: Success"

        # Simulate random failures on first attempt
        retry_count = req_data.get("retry_count", 0)

        if retry_count == 0:
            # 40% chance of failure on first try
            if random.random() < 0.4:
                req_data["retry_count"] = 1
                req_data["status"] = "Failed"
                _save_requests(requests)
                return f"Request {request_id} Status: Failed - Transient error, please retry verification"

        # Success on retry or lucky first attempt
        req_data["status"] = "Success"
        req_data["retry_count"] = retry_count + 1
        _save_requests(requests)

    return f"Request {request_id} Status: Success"


def get_all_db_state_for_eval() -> List[Dict]:
    """Helper for evaluator to see final state."""
    return _load_db()


def get_all_requests_for_eval() -> Dict:
    """Helper for evaluator to see requests."""
    return _load_requests()


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    # Reset DB for fresh run
    _reset_db()

    return [
        {
            "name": "list_entraid_users",
            "description": "Lists all users from EntraID. Returns list of users with id, name, and current_roles.",
            "function": list_entraid_users,
        },
        {
            "name": "get_role_instructions",
            "description": "Gets the unstructured role update instructions from HR/IT. Contains complex, sometimes ambiguous requirements.",
            "function": get_role_instructions,
        },
        {
            "name": "update_user_roles",
            "description": "Updates roles for a user. Returns a Request ID. RATE LIMITED: Max 3 calls per second, otherwise returns error. You must handle rate limit errors.",
            "function": update_user_roles,
        },
        {
            "name": "verify_request_status",
            "description": "Verifies the status of a specific Request ID. REQUIRED for all updates. May return 'Failed' on first attempt (transient errors) - you MUST retry failed verifications.",
            "function": verify_request_status,
        },
    ]
