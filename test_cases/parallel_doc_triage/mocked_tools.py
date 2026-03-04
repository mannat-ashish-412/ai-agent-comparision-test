"""Mocked tools for parallel document triage test case."""
import json
from pathlib import Path
from typing import List, Dict, Union
from pydantic import BaseModel


class ClassificationResult(BaseModel):
    issue_id: str
    classification: str
    confidence: float


class SimilarityResult(BaseModel):
    issue1_id: str
    issue2_id: str
    is_duplicate: bool
    similarity_score: float
    reasoning: str


class SeverityResult(BaseModel):
    issue_id: str
    severity: str
    reasoning: str


class ActionResult(BaseModel):
    issue_id: str
    next_action: str


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def classify_issue(issue_id: str, title: str, description: str) -> ClassificationResult:
    """Classifies a support ticket into standardized categories based on its content."""
    keywords_bug = ["crash", "error", "broken", "not working", "failing", "performance"]
    keywords_feature = ["add", "support", "would like", "request", "need ability"]
    keywords_question = ["how to", "where is", "can't find"]

    text = (title + " " + description).lower()

    if any(kw in text for kw in keywords_bug):
        return ClassificationResult(
            issue_id=issue_id, classification="bug", confidence=0.9
        )
    elif any(kw in text for kw in keywords_feature):
        return ClassificationResult(
            issue_id=issue_id, classification="feature", confidence=0.85
        )
    elif any(kw in text for kw in keywords_question):
        return ClassificationResult(
            issue_id=issue_id, classification="question", confidence=0.95
        )
    else:
        return ClassificationResult(
            issue_id=issue_id, classification="bug", confidence=0.5
        )


def check_similarity(issue1_id: str, issue2_id: str) -> SimilarityResult:
    """Analyzes the technical similarity between two issues to determine if they are potential duplicates."""
    input_data = load_input_data()
    items = {item["id"]: item for item in input_data.get("items", [])}

    issue1 = items.get(issue1_id)
    issue2 = items.get(issue2_id)

    if not issue1 or not issue2:
        return SimilarityResult(
            issue1_id=issue1_id,
            issue2_id=issue2_id,
            is_duplicate=False,
            similarity_score=0.0,
            reasoning="One or both issues not found",
        )

    text1 = (issue1["title"] + " " + issue1["description"]).lower()
    text2 = (issue2["title"] + " " + issue2["description"]).lower()

    words1 = set(text1.split())
    words2 = set(text2.split())
    overlap = (
        len(words1 & words2) / max(len(words1), len(words2)) if words1 and words2 else 0
    )

    is_duplicate = overlap > 0.4

    return SimilarityResult(
        issue1_id=issue1_id,
        issue2_id=issue2_id,
        is_duplicate=is_duplicate,
        similarity_score=overlap,
        reasoning=f"Keyword overlap: {overlap:.2%}",
    )


def assess_severity(
    issue_id: str, classification: str, title: str, description: str
) -> SeverityResult:
    """Evaluates the business impact and technical urgency of an issue to assign a severity level."""
    text = (title + " " + description).lower()

    if any(
        word in text for word in ["critical", "production", "all users", "database"]
    ):
        severity = "critical"
    elif any(word in text for word in ["crash", "failing", "cannot"]):
        severity = "high"
    elif classification == "bug":
        severity = "medium"
    else:
        severity = "low"

    return SeverityResult(
        issue_id=issue_id,
        severity=severity,
        reasoning=f"Based on keywords and classification: {classification}",
    )


def suggest_next_action(
    issue_id: str, classification: str, severity: str
) -> ActionResult:
    """Recommends the appropriate operational next step for an issue based on its category and severity."""
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
        ("question", "low"): "Add to support queue",
    }

    action = actions.get((classification, severity), "Review and categorize")
    return ActionResult(issue_id=issue_id, next_action=action)


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "classify_issue",
            "description": "Classifies a support ticket into standardized categories (bug, feature request, or question).",
            "function": classify_issue,
        },
        {
            "name": "check_similarity",
            "description": "Analyzes technical similarity between two issues to identify potential duplicates.",
            "function": check_similarity,
        },
        {
            "name": "assess_severity",
            "description": "Evaluates technical impact and business urgency to assign a severity level.",
            "function": assess_severity,
        },
        {
            "name": "suggest_next_action",
            "description": "Recommends the appropriate operational next step for an issue.",
            "function": suggest_next_action,
        },
    ]
