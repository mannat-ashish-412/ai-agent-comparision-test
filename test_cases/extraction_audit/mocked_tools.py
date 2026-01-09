"""Mocked tools for extraction and audit test case."""
import json
from pathlib import Path
from typing import List, Dict, Union
from pydantic import BaseModel


class Requirement(BaseModel):
    text: str
    category: str
    priority: str


class ExtractionResult(BaseModel):
    category: str
    requirements: List[Requirement]
    count: int


class ContradictionResult(BaseModel):
    req1: str
    req2: str
    is_contradiction: bool
    confidence: float
    reason: str


class ValidationResult(BaseModel):
    is_valid: bool
    present_sections: List[str]
    missing_sections: List[str]
    completeness: float


def load_input_data():
    """Load input data from the local input_data.json file."""
    path = Path(__file__).parent / "input_data.json"
    with open(path) as f:
        return json.load(f)


def extract_requirement(category: str) -> ExtractionResult:
    """Parses the source document to extract structured requirements for a specific functional area."""
    input_data = load_input_data()
    text = input_data.get("requirements_document", "")

    lines = text.split("\n")
    extracted_lines = []
    current_section = ""

    for line in lines:
        line = line.strip()
        if line.startswith("##"):
            current_section = line.lstrip("# ").lower()
        elif line.startswith("-") and category.lower() in current_section:
            extracted_lines.append(line.lstrip("- "))

    requirements = [
        Requirement(text=line, category=category, priority="medium")
        for line in extracted_lines
    ]

    return ExtractionResult(
        category=category, requirements=requirements, count=len(requirements)
    )


def detect_contradiction(req1: str, req2: str) -> ContradictionResult:
    """Analyzes two specific requirements to identify potential technical or logical conflicts."""
    negation_pairs = [
        (
            ["must", "require", "always", "all"],
            ["never", "no", "not", "guest", "optional"],
        ),
        (["immediately", "instant"], ["later", "after", "delay"]),
        (["store", "save", "keep"], ["never store", "don't store", "not store"]),
        (["indefinitely", "permanent"], ["minutes", "temporary", "limited"]),
        (["free"], ["cost", "$", "charge"]),
    ]

    req1_lower = req1.lower()
    req2_lower = req2.lower()

    is_contradiction = False
    reason = ""

    for positive_words, negative_words in negation_pairs:
        has_positive_1 = any(word in req1_lower for word in positive_words)
        has_negative_2 = any(word in req2_lower for word in negative_words)
        has_positive_2 = any(word in req2_lower for word in positive_words)
        has_negative_1 = any(word in req1_lower for word in negative_words)

        if (has_positive_1 and has_negative_2) or (has_positive_2 and has_negative_1):
            is_contradiction = True
            reason = "Conflicting requirements: one requires action, other prohibits it"
            break

    return ContradictionResult(
        req1=req1,
        req2=req2,
        is_contradiction=is_contradiction,
        confidence=0.8 if is_contradiction else 0.3,
        reason=reason if is_contradiction else "No clear contradiction detected",
    )


def assess_severity(contradiction: ContradictionResult) -> str:
    """Evaluates the business impact and risk of a detected contradiction to assign a severity level."""
    req_text = (contradiction.req1 + " " + contradiction.req2).lower()

    if any(
        word in req_text for word in ["security", "authentication", "payment", "pci"]
    ):
        return "high"
    elif any(
        word in req_text for word in ["fraud", "inventory", "tracking", "oversell"]
    ):
        return "high"
    elif any(word in req_text for word in ["shipping", "confirmation", "returns"]):
        return "medium"
    else:
        return "low"


def generate_clarifying_question(contradiction: ContradictionResult) -> str:
    """Formulates a professional question for stakeholders to resolve an identified requirement conflict."""
    req1 = contradiction.req1
    req2 = contradiction.req2

    return f"The requirements state both '{req1}' and '{req2}'. Which requirement should take precedence, or how should these be reconciled?"


def validate_prd_structure(prd: Dict[str, List[str]]) -> ValidationResult:
    """Verifies that the consolidated PRD document contains all mandatory functional sections."""
    required_sections = [
        "authentication",
        "payment",
        "shipping",
        "inventory",
        "confirmation",
        "returns",
    ]

    present_sections = list(prd.keys())
    missing_sections = [s for s in required_sections if s not in present_sections]

    is_valid = len(missing_sections) == 0

    return ValidationResult(
        is_valid=is_valid,
        present_sections=present_sections,
        missing_sections=missing_sections,
        completeness=len(present_sections) / len(required_sections),
    )


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "extract_requirement",
            "description": "Extracts structured requirements for a specific functional area from the source document.",
            "function": extract_requirement,
        },
        {
            "name": "detect_contradiction",
            "description": "Identifies potential technical or logical conflicts between two requirements.",
            "function": detect_contradiction,
        },
        {
            "name": "assess_severity",
            "description": "Evaluates the business risk and impact of an identified requirement conflict.",
            "function": assess_severity,
        },
        {
            "name": "generate_clarifying_question",
            "description": "Generates a professional clarifying question to help stakeholders resolve a conflict.",
            "function": generate_clarifying_question,
        },
        {
            "name": "validate_prd_structure",
            "description": "Ensures the final PRD meets the mandatory structural standards and section requirements.",
            "function": validate_prd_structure,
        },
    ]
