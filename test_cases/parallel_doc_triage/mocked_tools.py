"""
Mocked tools for parallel document triage test case.
"""
from typing import List, Dict, Any
import random


def classify_issue(issue_id: str, title: str, description: str) -> Dict[str, str]:
    """
    Classify an issue as bug, feature, or question.
    
    Args:
        issue_id: Unique identifier for the issue
        title: Issue title
        description: Issue description
        
    Returns:
        Classification result with type and confidence
    """
    # Mock classification logic
    keywords_bug = ['crash', 'error', 'broken', 'not working', 'failing']
    keywords_feature = ['add', 'support', 'would like', 'request', 'need ability']
    keywords_question = ['how to', 'where is', "can't find"]
    
    text = (title + " " + description).lower()
    
    if any(kw in text for kw in keywords_bug):
        return {
            "issue_id": issue_id,
            "classification": "bug",
            "confidence": 0.9
        }
    elif any(kw in text for kw in keywords_feature):
        return {
            "issue_id": issue_id,
            "classification": "feature",
            "confidence": 0.85
        }
    elif any(kw in text for kw in keywords_question):
        return {
            "issue_id": issue_id,
            "classification": "question",
            "confidence": 0.95
        }
    else:
        return {
            "issue_id": issue_id,
            "classification": "bug",
            "confidence": 0.5
        }


def check_similarity(issue1: Dict[str, Any], issue2: Dict[str, Any]) -> Dict[str, Any]:
    """
    Check if two issues are duplicates.
    
    Args:
        issue1: First issue
        issue2: Second issue
        
    Returns:
        Similarity result with score and reasoning
    """
    # Mock similarity detection
    text1 = (issue1['title'] + " " + issue1['description']).lower()
    text2 = (issue2['title'] + " " + issue2['description']).lower()
    
    # Simple keyword overlap
    words1 = set(text1.split())
    words2 = set(text2.split())
    overlap = len(words1 & words2) / max(len(words1), len(words2))
    
    is_duplicate = overlap > 0.4
    
    return {
        "issue1_id": issue1['id'],
        "issue2_id": issue2['id'],
        "is_duplicate": is_duplicate,
        "similarity_score": overlap,
        "reasoning": f"Keyword overlap: {overlap:.2%}"
    }


def assess_severity(
    issue_id: str, 
    classification: str, 
    title: str, 
    description: str
) -> Dict[str, str]:
    """
    Assess the severity of an issue.
    
    Args:
        issue_id: Unique identifier
        classification: Issue type (bug/feature/question)
        title: Issue title
        description: Issue description
        
    Returns:
        Severity assessment
    """
    text = (title + " " + description).lower()
    
    # Critical indicators
    if any(word in text for word in ['critical', 'production', 'all users', 'database']):
        severity = "critical"
    # High severity indicators
    elif any(word in text for word in ['crash', 'failing', 'cannot']):
        severity = "high"
    # Medium severity
    elif classification == "bug":
        severity = "medium"
    # Low severity for features and questions
    else:
        severity = "low"
    
    return {
        "issue_id": issue_id,
        "severity": severity,
        "reasoning": f"Based on keywords and classification: {classification}"
    }


def suggest_next_action(
    issue_id: str,
    classification: str,
    severity: str
) -> Dict[str, str]:
    """
    Suggest next action for an issue.
    
    Args:
        issue_id: Unique identifier
        classification: Issue type
        severity: Severity level
        
    Returns:
        Next action suggestion
    """
    actions = {
        ("bug", "critical"): "Immediate investigation and hotfix required",
        ("bug", "high"): "Assign to engineering team for urgent fix",
        ("bug", "medium"): "Add to current sprint backlog",
        ("bug", "low"): "Add to backlog for future sprint",
        ("feature", "critical"): "Escalate to product team",
        ("feature", "high"): "Review in next planning meeting",
        ("feature", "medium"): "Add to feature backlog",
        ("feature", "low"): "Add to feature backlog",
        ("question", "critical"): "Provide immediate support response",
        ("question", "high"): "Respond within 24 hours",
        ("question", "medium"): "Respond within 48 hours",
        ("question", "low"): "Add to support queue"
    }
    
    action = actions.get((classification, severity), "Review and categorize")
    
    return {
        "issue_id": issue_id,
        "next_action": action
    }


def get_tools() -> List[Dict[str, Any]]:
    """
    Get list of available tools for this test case.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "classify_issue",
            "description": "Classify an issue as bug, feature, or question",
            "function": classify_issue
        },
        {
            "name": "check_similarity",
            "description": "Check if two issues are duplicates",
            "function": check_similarity
        },
        {
            "name": "assess_severity",
            "description": "Assess the severity of an issue",
            "function": assess_severity
        },
        {
            "name": "suggest_next_action",
            "description": "Suggest next action for an issue",
            "function": suggest_next_action
        }
    ]
