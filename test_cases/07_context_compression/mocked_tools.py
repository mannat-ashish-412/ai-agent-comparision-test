"""Mocked tools for context compression test."""
from typing import Dict, Any, List

def extract_key_facts(messages: List[Dict]) -> List[str]:
    facts = []
    for msg in messages:
        if "PostgreSQL" in msg.get("content", ""):
            facts.append("Database: PostgreSQL")
        if "RDS" in msg.get("content", ""):
            facts.append("Database: RDS (updated)")
        if "db.t3.medium" in msg.get("content", ""):
            facts.append("Instance: db.t3.medium")
    return facts

def summarize_conversation(messages: List[Dict]) -> str:
    return "User wants to deploy FastAPI microservice on AWS ECS Fargate with RDS PostgreSQL (db.t3.medium, Multi-AZ) in us-east-1."

def get_tools() -> List[Dict[str, Any]]:
    return [
        {"name": "extract_key_facts", "function": extract_key_facts},
        {"name": "summarize_conversation", "function": summarize_conversation}
    ]
