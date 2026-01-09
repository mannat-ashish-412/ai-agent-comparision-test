"""Evaluator for planner-workers-join test."""
from typing import Dict, Any

def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {"correctness": 0.0, "consistency": 0.0, "conflict_handling": 0.0, "traceability": 0.0}
    if not isinstance(actual_output, dict):
        return scores
    
    # Correctness
    if "subtasks" in actual_output and len(actual_output["subtasks"]) == 3:
        scores["correctness"] += 40
    if "merged_plan" in actual_output:
        scores["correctness"] += 60
    
    # Consistency
    if "consistency_check" in actual_output:
        scores["consistency"] = 100
    else:
        scores["consistency"] = 50
    
    # Conflict handling
    if "subtask_results" in actual_output and len(actual_output["subtask_results"]) >= 3:
        scores["conflict_handling"] = 80
    
    # Traceability
    if "subtasks" in actual_output and "merged_plan" in actual_output:
        scores["traceability"] = 90
    
    return scores
