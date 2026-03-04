"""Evaluator for entraid roles update test."""
from typing import Any, Dict
import json
from pathlib import Path
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Dict[str, Any], expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    # 1. Load Real State (Simulated DB and Requests)
    db_path = Path(__file__).parent / "simulated_db.json"
    requests_path = Path(__file__).parent / "simulated_requests.json"

    real_db_state = []
    if db_path.exists():
        with open(db_path, "r") as f:
            try:
                real_db_state = json.load(f)
            except Exception:
                pass

    real_requests_state = {}
    if requests_path.exists():
        with open(requests_path, "r") as f:
            try:
                real_requests_state = json.load(f)
            except Exception:
                pass

    # 2. Define Ground Truth - Correct interpretation of complex instructions
    # user_001: Sarah Connor - Admin + Viewer (keep existing)
    # user_002: John Smith - Editor + Contributor + Auditor
    # user_003: Kyle Reese - Viewer only (REVOKE Editor, security incident)
    # user_004: Marcus Wright - Editor only (REMOVE Admin per latest email)
    # user_005: Kate Brewster - Admin + Editor + Contributor
    # user_006: Derek Reese - Viewer only (REVOKE Auditor, security concern)
    # user_007: Cameron Phillips - Editor + Contributor (has Editor, needs Contributor)
    # user_008: James Ellison - Viewer + Auditor (compliance rule)
    # user_009: Catherine Weaver - Admin + Editor + Contributor + Viewer + Auditor (CEO, ALL roles)
    # user_010: Savannah Weaver - Viewer only (intern)
    # user_011: Charley Dixon - [] empty (REVOKE ALL ACCESS)
    # user_012: Jesse Flores - Viewer + Auditor (same dept as James, compliance rule)

    expected_roles_map = {
        "user_001": {"Admin", "Viewer"},
        "user_002": {"Editor", "Contributor", "Auditor"},
        "user_003": {"Viewer"},
        "user_004": {"Editor"},
        "user_005": {"Admin", "Editor", "Contributor"},
        "user_006": {"Viewer"},
        "user_007": {"Editor", "Contributor"},
        "user_008": {"Viewer", "Auditor"},
        "user_009": {"Admin", "Editor", "Contributor", "Viewer", "Auditor"},
        "user_010": {"Viewer"},
        "user_011": set(),  # Empty - all access revoked
        "user_012": {"Viewer", "Auditor"},
    }

    # 3. Validation Logic
    correctness_issues = []

    # Check DB state
    processed_count = 0
    for user in real_db_state:
        uid = user.get("id")
        roles = set(user.get("assigned_roles", []))
        if uid in expected_roles_map:
            processed_count += 1
            expected = expected_roles_map[uid]
            if roles != expected:
                correctness_issues.append(
                    f"User {uid} has wrong roles. Expected {expected}, got {roles}"
                )
        else:
            correctness_issues.append(f"Unexpected user {uid} in DB")

    if processed_count < 12:
        correctness_issues.append(
            f"Only processed {processed_count}/12 users. but all 12 users should be processed"
        )

    # Check Verification (Requests) - all must be Success
    verification_issues = json.dumps(real_requests_state)

    success = len(correctness_issues) == 0 and len(verification_issues) == 0

    # 4. LLM Judge Rubrics
    rubrics = [
        (
            "correctness",
            f"Evaluate correctness. Did the agent correctly interpret the complex, ambiguous instructions? Issues: {correctness_issues}",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent handle conflicting information correctly (e.g., Marcus Wright's conflicting reports)?",
        ),
        (
            "traceability",
            f"Evaluate traceability. Agent claimed processed users: {actual_output.get('processed_users')}. Actual DB users: {[u['id'] for u in real_db_state]}",
        ),
        (
            "verification",
            f"Evaluate verification. Did the agent retry failed verifications and handle rate limits? Issues: {verification_issues}. Agent reported all_verified: {actual_output.get('all_requests_verified')}",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Hard overrides
    scores["passed"] = success
    if not success:
        scores["correctness"] = 50.0 if len(correctness_issues) > 0 else 100.0
        scores["verification"] = 0.0 if len(verification_issues) > 0 else 100.0

    return scores
