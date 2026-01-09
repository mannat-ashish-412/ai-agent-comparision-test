"""Mocked tools for RCA test."""
import json
from pathlib import Path
from typing import Dict, List, Union
from pydantic import BaseModel


class AnalysisResult(BaseModel):
    likely_cause: str
    confidence: float


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def analyze_stack_trace() -> AnalysisResult:
    """Performs a diagnostic analysis of the CI/CD pipeline logs to identify root cause failure patterns."""
    return AnalysisResult(
        likely_cause="The email validation logic is rejecting valid email addresses that contain a '+' sign (plus addressing).",
        confidence=0.95,
    )


def generate_diff(original: str, fixed: str) -> str:
    """Generates a standard unified diff representation for a proposed code correction."""
    return f"- {original}\n+ {fixed}"


def create_test_case(scenario: str) -> str:
    """Generates a Python-based regression test case for a specific edge case or bug scenario."""
    if "plus" in scenario:
        return f"def test_{scenario}():\n    assert validate_email('user+test@example.com') is True"
    return f"def test_{scenario}():\n    assert validate_email('standard@example.com') is True"


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "analyze_stack_trace",
            "description": "Diagnoses CI pipeline failures by identifying underlying root causes from execution logs.",
            "function": analyze_stack_trace,
        },
        {
            "name": "generate_diff",
            "description": "Produces a standardized diff for proposed code changes.",
            "function": generate_diff,
        },
        {
            "name": "create_test_case",
            "description": "Automates the creation of regression test functions for identified bug scenarios.",
            "function": create_test_case,
        },
    ]
