"""Mocked tools for planner-workers-join test."""
import json
from pathlib import Path
from typing import Dict, List, Union
from pydantic import BaseModel


class AnalysisResult(BaseModel):
    focus: str
    recommendations: List[str] = []
    patterns: List[Dict[str, str]] = []
    steps: List[str] = []


class ConsistencyResult(BaseModel):
    is_consistent: bool
    conflicts: List[str]
    notes: str


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def analyze_schema(focus: str) -> AnalysisResult:
    """Provides a detailed technical analysis of the database schema for a specific architectural area.

    The analysis includes specific recommendations, data patterns, or implementation steps
    required for a successful migration.
    """
    if focus == "data_modeling":
        return AnalysisResult(
            focus="data_modeling",
            recommendations=[
                "Use composite primary key (PK: user_id, SK: order_id) for orders",
                "Create GSI on email for user lookups",
                "Denormalize product info in orders for faster access",
            ],
        )
    elif focus == "access_patterns":
        return AnalysisResult(
            focus="access_patterns",
            patterns=[
                {"pattern": "GetUserByEmail", "solution": "GSI on email"},
                {"pattern": "GetOrdersByUser", "solution": "Query on PK"},
                {"pattern": "GetProductBySKU", "solution": "PK on SKU"},
            ],
        )
    else:
        return AnalysisResult(
            focus="migration_steps",
            steps=[
                "1. Create DynamoDB tables",
                "2. Set up data pipeline",
                "3. Migrate historical data",
                "4. Enable dual writes",
                "5. Switch reads to DynamoDB",
                "6. Decommission MongoDB",
            ],
        )


def check_consistency(plans: List[Dict]) -> ConsistencyResult:
    """Validates technical consistency between multiple architectural plan sections.

    Ensures that recommendations in one area (e.g., data modeling) are compatible
    with decisions made in others (e.g., access patterns).
    """
    return ConsistencyResult(
        is_consistent=True, conflicts=[], notes="All technical sections are compatible."
    )


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "analyze_schema",
            "description": "Provides specialized technical analysis of the database schema for a specific architectural focus area.",
            "function": analyze_schema,
        },
        {
            "name": "check_consistency",
            "description": "Verifies that multiple technical plan sections are consistent and compatible with each other.",
            "function": check_consistency,
        },
    ]
