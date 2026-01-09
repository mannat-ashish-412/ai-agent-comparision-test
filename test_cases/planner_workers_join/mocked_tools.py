"""Mocked tools for planner-workers-join test."""
from typing import Dict, Any, List

def analyze_schema(schema: Dict[str, Any], focus: str) -> Dict[str, Any]:
    """Analyze schema for specific aspect."""
    if focus == "data_modeling":
        return {
            "focus": "data_modeling",
            "recommendations": [
                "Use composite primary key (PK: user_id, SK: order_id) for orders",
                "Create GSI on email for user lookups",
                "Denormalize product info in orders for faster access"
            ]
        }
    elif focus == "access_patterns":
        return {
            "focus": "access_patterns",
            "patterns": [
                {"pattern": "GetUserByEmail", "solution": "GSI on email"},
                {"pattern": "GetOrdersByUser", "solution": "Query on PK"},
                {"pattern": "GetProductBySKU", "solution": "PK on SKU"}
            ]
        }
    else:
        return {
            "focus": "migration_steps",
            "steps": [
                "1. Create DynamoDB tables",
                "2. Set up data pipeline",
                "3. Migrate historical data",
                "4. Enable dual writes",
                "5. Switch reads to DynamoDB",
                "6. Decommission MongoDB"
            ]
        }

def check_consistency(plan1: Dict, plan2: Dict) -> Dict[str, Any]:
    """Check consistency between two plan sections."""
    return {
        "is_consistent": True,
        "conflicts": [],
        "notes": "Plans are compatible"
    }

def get_tools() -> List[Dict[str, Any]]:
    return [
        {"name": "analyze_schema", "function": analyze_schema},
        {"name": "check_consistency", "function": check_consistency}
    ]
