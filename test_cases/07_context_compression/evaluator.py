"""Evaluator for context compression test."""
from typing import Dict, Any

def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {"correctness": 0.0, "consistency": 0.0, "conflict_handling": 0.0, "traceability": 0.0}
    if not isinstance(actual_output, dict):
        return scores
    
    # Correctness
    if "compressed_state" in actual_output:
        scores["correctness"] += 30
    if "final_answer" in actual_output:
        answer = str(actual_output["final_answer"]).lower()
        if "rds" in answer:
            scores["correctness"] += 35
        if "db.t3.medium" in answer or "t3.medium" in answer:
            scores["correctness"] += 35
    
    # Consistency
    if "final_answer" in actual_output:
        answer = str(actual_output["final_answer"]).lower()
        # Should mention RDS, not self-managed
        if "rds" in answer and "self-managed" not in answer:
            scores["consistency"] = 90
        elif "rds" in answer:
            scores["consistency"] = 70
    
    # Conflict handling
    if "compressed_state" in actual_output or "key_facts" in actual_output:
        state_str = str(actual_output.get("compressed_state", "")) + str(actual_output.get("key_facts", ""))
        if "rds" in state_str.lower():
            scores["conflict_handling"] = 85
    
    # Traceability
    if "sources" in actual_output:
        scores["traceability"] = 90
    elif "compressed_state" in actual_output and "final_answer" in actual_output:
        scores["traceability"] = 70
    
    return scores
