"""Evaluator for planner-workers-join test."""
from typing import Dict, Any


def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {
        "correctness": 0.0,
        "consistency": 0.0,
        "conflict_handling": 0.0,
        "traceability": 100.0,
    }
    if not isinstance(actual_output, dict):
        scores["passed"] = False
        return scores

    # Correctness: Check if unified plan and findings exist
    if "unified_plan" in actual_output:
        scores["correctness"] += 50

    if "findings_by_area" in actual_output:
        findings = actual_output["findings_by_area"]
        # Should have findings for all 3 areas
        areas = ["data_modeling", "access_patterns", "migration_steps"]
        found_areas = sum(1 for area in areas if area in findings)
        scores["correctness"] += (found_areas / 3) * 50

    # Consistency
    if "consistency_check" in actual_output:
        scores["consistency"] = 100

    # Conflict handling: Check if unified plan is substantive
    if (
        "unified_plan" in actual_output
        and len(str(actual_output["unified_plan"])) > 100
    ):
        scores["conflict_handling"] = 100

    # Pass criteria: All scores ≥ 70
    scores["passed"] = (
        all(
            score >= 70
            for score in [
                scores["correctness"],
                scores["consistency"],
                scores["conflict_handling"],
            ]
        )
        and "unified_plan" in actual_output
        and len(actual_output.get("findings_by_area", {})) >= 3
    )

    return scores
