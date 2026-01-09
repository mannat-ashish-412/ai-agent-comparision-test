"""Mocked tools for context compression test."""
import json
from pathlib import Path
from typing import Dict, List, Union


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def extract_key_facts() -> List[str]:
    """Scans the conversation history to extract key technical requirements and architectural decisions."""
    input_data = load_input_data()
    messages = input_data.get("conversation_history", [])

    facts = []
    for msg in messages:
        content = msg.get("content", "")
        if "PostgreSQL" in content:
            facts.append("Database Engine: PostgreSQL")
        if "RDS" in content:
            facts.append("Deployment Model: AWS RDS")
        if "db.t3.medium" in content:
            facts.append("Instance Type: db.t3.medium")
        if "ECS Fargate" in content:
            facts.append("Platform: AWS ECS Fargate")
        if "us-east-1" in content:
            facts.append("Region: us-east-1")

    return list(dict.fromkeys(facts))


def summarize_conversation() -> str:
    """Generates a high-level technical summary of the project discussion and agreed-upon requirements."""
    return "The user is planning to deploy a Python FastAPI microservice on AWS using ECS Fargate, fronted by an Application Load Balancer with ACM SSL. The database will be a production AWS RDS PostgreSQL instance using a db.t3.medium size with Multi-AZ enabled in us-east-1."


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "extract_key_facts",
            "description": "Identifies and extracts critical technical facts and decisions from the conversation history.",
            "function": extract_key_facts,
        },
        {
            "name": "summarize_conversation",
            "description": "Produces a concise high-level summary of the architectural and project-related discussion.",
            "function": summarize_conversation,
        },
    ]
