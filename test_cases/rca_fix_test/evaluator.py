"""Evaluator for RCA test."""
from typing import Dict, Any

def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {"correctness": 0.0, "consistency": 0.0, "conflict_handling": 70.0, "traceability": 0.0}
    if not isinstance(actual_output, dict):
        return scores
    
    if "root_cause" in actual_output and "+" in str(actual_output["root_cause"]).lower():
        scores["correctness"] += 35
    if "proposed_patch" in actual_output:
        scores["correctness"] += 35
    if "regression_tests" in actual_output and len(actual_output["regression_tests"]) >= 2:
        scores["correctness"] += 30
    
    if "proposed_patch" in actual_output and "root_cause" in actual_output:
        scores["consistency"] = 90
    
    output_str = str(actual_output).lower()
    if any(word in output_str for word in ["debugger", "fixer", "tester", "agent"]):
        scores["traceability"] = 85
    
    return scores
