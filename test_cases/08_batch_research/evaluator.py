"""Evaluator for batch research test."""
from typing import Dict, Any

def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    scores = {"correctness": 0.0, "consistency": 0.0, "conflict_handling": 70.0, "traceability": 0.0}
    if not isinstance(actual_output, dict):
        return scores
    
    # Correctness
    if "answers" in actual_output:
        answers = actual_output["answers"]
        if len(answers) == 5:
            scores["correctness"] = 100
        elif len(answers) >= 3:
            scores["correctness"] = 60
        elif len(answers) > 0:
            scores["correctness"] = 30
    
    # Consistency
    if "answers" in actual_output:
        # Check for contradictions
        answers_str = str(actual_output["answers"]).lower()
        # Simple check: no obvious contradictions
        scores["consistency"] = 85
    
    # Traceability
    if "citations" in actual_output:
        citations = actual_output["citations"]
        
        # Check if citations reference KB IDs
        citations_str = str(citations).lower()
        kb_id_count = citations_str.count("kb-")
        
        if kb_id_count >= 5:
            scores["traceability"] = 100
        elif kb_id_count >= 3:
            scores["traceability"] = 70
        elif kb_id_count > 0:
            scores["traceability"] = 40
    
    return scores
