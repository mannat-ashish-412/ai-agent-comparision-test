"""Evaluator for RCA test."""
from typing import Dict, Any


def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {
        "correctness": 0.0,
        "consistency": 0.0,
        "conflict_handling": 70.0,
        "traceability": 100.0,
    }
    if not isinstance(actual_output, dict):
        scores["passed"] = False
        return scores

    # Correctness: Check for root cause, patch, and regression tests
    if (
        "root_cause" in actual_output
        and "+" in str(actual_output["root_cause"]).lower()
    ):
        scores["correctness"] += 35
    elif "root_cause" in actual_output:
        scores["correctness"] += 20

    if "proposed_patch" in actual_output:
        scores["correctness"] += 35
    if (
        "regression_tests" in actual_output
        and len(actual_output["regression_tests"]) >= 2
    ):
        scores["correctness"] += 30

    # Consistency: Fix should match root cause
    if "proposed_patch" in actual_output and "root_cause" in actual_output:
        scores["consistency"] = 100

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
        and "root_cause" in actual_output
        and "proposed_patch" in actual_output
        and len(actual_output.get("regression_tests", [])) >= 2
    )

    return scores
