"""Mocked tools for batch research test."""
import json
from pathlib import Path
from typing import Dict, List, Optional, Union
from pydantic import BaseModel


class SearchResult(BaseModel):
    snippet_id: Optional[str]
    content: str
    relevance: float


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def search_knowledge_base(query: str) -> SearchResult:
    """Searches the centralized corporate knowledge base for specific policy documentation or organizational guidelines."""
    input_data = load_input_data()
    kb = input_data.get("knowledge_base", [])

    query_lower = query.lower()
    for item in kb:
        content_lower = item["content"].lower()
        if "remote" in query_lower and "remote" in content_lower:
            return SearchResult(
                snippet_id=item["id"], content=item["content"], relevance=0.95
            )
        elif (
            "vacation days" in query_lower
            and "vacation" in content_lower
            and "days" in content_lower
        ):
            return SearchResult(
                snippet_id=item["id"], content=item["content"], relevance=0.90
            )
        elif "requesting" in query_lower and "request" in content_lower:
            return SearchResult(
                snippet_id=item["id"], content=item["content"], relevance=0.88
            )
        elif "blackout" in query_lower and "blackout" in content_lower:
            return SearchResult(
                snippet_id=item["id"], content=item["content"], relevance=0.92
            )
        elif "unused" in query_lower and "unused" in content_lower:
            return SearchResult(
                snippet_id=item["id"], content=item["content"], relevance=0.87
            )

    return SearchResult(
        snippet_id=None, content="No relevant information found", relevance=0.0
    )


def extract_answer(snippet: str, question: str) -> str:
    """Extracts a precise, context-aware answer from a technical or policy-related text snippet."""
    if "remote" in question.lower():
        return (
            "Employees may work remotely up to 3 days per week with manager approval."
        )
    elif "vacation days" in question.lower():
        return "Full-time employees receive 15 vacation days per year."
    elif "requesting" in question.lower() or "process" in question.lower():
        return "Submit requests through HR portal at least 2 weeks in advance."
    elif "blackout" in question.lower():
        return "Q4 (Oct-Dec) requires director-level approval for vacation."
    elif "unused" in question.lower():
        return "Up to 5 unused days roll over to next year, must be used in Q1."
    return "Information not available."


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "search_knowledge_base",
            "description": "Searches the internal company knowledge base for policy and guideline documentation.",
            "function": search_knowledge_base,
        },
        {
            "name": "extract_answer",
            "description": "Extracts a specific answer from a technical or policy-related snippet based on the user's question.",
            "function": extract_answer,
        },
    ]
