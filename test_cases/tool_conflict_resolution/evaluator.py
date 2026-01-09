"""
Evaluator for tool conflict resolution test case.
"""
from typing import Dict, Any


def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    """Evaluate conflict resolution output."""
    scores = {
        "correctness": 0.0,
        "consistency": 0.0,
        "conflict_handling": 0.0,
        "traceability": 0.0,
    }

    if not isinstance(actual_output, dict):
        return scores

    # Correctness
    correctness_points = 0

    if "detected_conflicts" in actual_output:
        conflicts = actual_output["detected_conflicts"]
        if len(conflicts) > 0:
            correctness_points += 30

    if "resolution_policy" in actual_output:
        policy = actual_output["resolution_policy"]
        valid_policies = expected_output["valid_resolution_policies"]
        if any(vp in str(policy).lower() for vp in valid_policies):
            correctness_points += 30

    if "final_price" in actual_output:
        price = actual_output["final_price"]
        if price in [999, 1099]:  # Must match one of the conflicting sources
            correctness_points += 40

    scores["correctness"] = min(correctness_points, 100)

    # Consistency
    consistency_points = 100

    if "final_price" in actual_output and "resolution_policy" in actual_output:
        price = actual_output["final_price"]
        policy = str(actual_output["resolution_policy"]).lower()

        # Check policy matches price choice
        if price == 999 and "catalog" in policy:
            consistency_points -= 40
        elif price == 1099 and ("api" in policy or "fresh" in policy):
            consistency_points -= 40

    scores["consistency"] = max(consistency_points, 0)

    # Conflict Handling
    conflict_points = 0

    if "detected_conflicts" in actual_output:
        conflicts = actual_output["detected_conflicts"]
        if len(conflicts) > 0:
            conflict_points += 50

            # Check for details
            for conflict in conflicts:
                if isinstance(conflict, dict):
                    has_sources = any(
                        k in conflict for k in ["source1", "source2", "sources"]
                    )
                    has_values = any(
                        k in conflict for k in ["value1", "value2", "values"]
                    )
                    if has_sources and has_values:
                        conflict_points += 25
                        break

    if "resolution_policy" in actual_output:
        conflict_points += 25

    scores["conflict_handling"] = min(conflict_points, 100)

    # Traceability
    trace_points = 0

    if "audit_trail" in actual_output:
        trace_points += 50

        audit = str(actual_output["audit_trail"]).lower()
        # Should mention sources
        if any(word in audit for word in ["api", "database", "catalog", "cache"]):
            trace_points += 20

        # Should mention reasoning
        if any(
            word in audit
            for word in ["because", "reason", "chose", "selected", "policy"]
        ):
            trace_points += 30

    scores["traceability"] = min(trace_points, 100)

    # Pass criteria: All scores ≥ 70
    scores["passed"] = all(
        score >= 70
        for score in [
            scores["correctness"],
            scores["consistency"],
            scores["conflict_handling"],
            scores["traceability"],
        ]
    )

    return scores
