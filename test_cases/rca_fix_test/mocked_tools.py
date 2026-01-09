"""Mocked tools for RCA test."""
from typing import Dict, Any, List

def analyze_stack_trace(log: str) -> Dict[str, Any]:
    return {"likely_cause": "Email validation rejecting valid characters", "confidence": 0.9}

def generate_diff(original: str, fixed: str) -> str:
    return f"- {original}\n+ {fixed}"

def create_test_case(scenario: str) -> str:
    return f"def test_{scenario}():\n    assert validate_email('user+test@example.com') == True"

def get_tools() -> List[Dict[str, Any]]:
    return [
        {"name": "analyze_stack_trace", "function": analyze_stack_trace},
        {"name": "generate_diff", "function": generate_diff},
        {"name": "create_test_case", "function": create_test_case}
    ]
