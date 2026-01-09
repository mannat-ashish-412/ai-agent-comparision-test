"""Mocked tools for batch research test."""
from typing import Dict, Any, List

def search_knowledge_base(query: str, kb: List[Dict]) -> Dict[str, Any]:
    """Search KB for relevant snippet."""
    query_lower = query.lower()
    
    # Simple keyword matching
    for item in kb:
        content_lower = item["content"].lower()
        if "remote" in query_lower and "remote" in content_lower:
            return {"snippet_id": item["id"], "content": item["content"], "relevance": 0.95}
        elif "vacation days" in query_lower and "vacation" in content_lower and "days" in content_lower:
            return {"snippet_id": item["id"], "content": item["content"], "relevance": 0.90}
        elif "requesting" in query_lower and "request" in content_lower:
            return {"snippet_id": item["id"], "content": item["content"], "relevance": 0.88}
        elif "blackout" in query_lower and "blackout" in content_lower:
            return {"snippet_id": item["id"], "content": item["content"], "relevance": 0.92}
        elif "unused" in query_lower and "unused" in content_lower:
            return {"snippet_id": item["id"], "content": item["content"], "relevance": 0.87}
    
    return {"snippet_id": None, "content": "No relevant information found", "relevance": 0.0}

def extract_answer(snippet: str, question: str) -> str:
    """Extract answer from snippet."""
    # Simple extraction
    if "remote" in question.lower():
        return "Employees may work remotely up to 3 days per week with manager approval."
    elif "vacation days" in question.lower():
        return "Full-time employees receive 15 vacation days per year."
    elif "requesting" in question.lower() or "process" in question.lower():
        return "Submit requests through HR portal at least 2 weeks in advance."
    elif "blackout" in question.lower():
        return "Q4 (Oct-Dec) requires director-level approval for vacation."
    elif "unused" in question.lower():
        return "Up to 5 unused days roll over to next year, must be used in Q1."
    return "Information not available."

def get_tools() -> List[Dict[str, Any]]:
    return [
        {"name": "search_knowledge_base", "function": search_knowledge_base},
        {"name": "extract_answer", "function": extract_answer}
    ]
