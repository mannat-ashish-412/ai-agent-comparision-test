"""
Mocked tools for extraction and audit test case.
"""
from typing import List, Dict, Any, Optional


def extract_requirement(text: str, category: str) -> Dict[str, Any]:
    """
    Extract a structured requirement from text.
    
    Args:
        text: Text containing the requirement
        category: Category (authentication, payment, shipping, etc.)
        
    Returns:
        Structured requirement
    """
    # Simple extraction based on keywords
    lines = [line.strip() for line in text.split('\n') if line.strip() and line.strip().startswith('-')]
    
    requirements = []
    for line in lines:
        line = line.lstrip('- ')
        if line:
            requirements.append({
                "text": line,
                "category": category,
                "priority": "medium"
            })
    
    return {
        "category": category,
        "requirements": requirements,
        "count": len(requirements)
    }


def detect_contradiction(req1: str, req2: str) -> Dict[str, Any]:
    """
    Detect if two requirements contradict each other.
    
    Args:
        req1: First requirement text
        req2: Second requirement text
        
    Returns:
        Contradiction analysis
    """
    # Simple contradiction detection based on negation keywords
    negation_pairs = [
        (['must', 'require', 'always', 'all'], ['never', 'no', 'not', 'guest', 'optional']),
        (['immediately', 'instant'], ['later', 'after', 'delay']),
        (['store', 'save', 'keep'], ['never store', 'don\'t store', 'not store']),
        (['indefinitely', 'permanent'], ['minutes', 'temporary', 'limited']),
        (['free'], ['cost', '$', 'charge']),
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
            reason = f"Conflicting requirements: one requires action, other prohibits it"
            break
    
    return {
        "req1": req1,
        "req2": req2,
        "is_contradiction": is_contradiction,
        "confidence": 0.8 if is_contradiction else 0.3,
        "reason": reason if is_contradiction else "No clear contradiction detected"
    }


def assess_severity(contradiction: Dict[str, Any]) -> str:
    """
    Assess the severity of a contradiction.
    
    Args:
        contradiction: Contradiction details
        
    Returns:
        Severity level (critical/high/medium/low)
    """
    req_text = (contradiction.get('req1', '') + ' ' + contradiction.get('req2', '')).lower()
    
    if any(word in req_text for word in ['security', 'authentication', 'payment', 'pci']):
        return "high"
    elif any(word in req_text for word in ['fraud', 'inventory', 'tracking']):
        return "medium"
    else:
        return "low"


def generate_clarifying_question(
    contradiction: Dict[str, Any],
    context: Optional[str] = None
) -> str:
    """
    Generate a clarifying question for a contradiction.
    
    Args:
        contradiction: Contradiction details
        context: Additional context
        
    Returns:
        Clarifying question
    """
    req1 = contradiction.get('req1', '')
    req2 = contradiction.get('req2', '')
    
    # Generate question based on contradiction
    question = f"The requirements state both '{req1[:50]}...' and '{req2[:50]}...'. Which requirement should take precedence, or should these be reconciled differently?"
    
    return question


def validate_prd_structure(prd: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate that PRD has required structure.
    
    Args:
        prd: Product requirements document
        
    Returns:
        Validation result
    """
    required_sections = [
        'authentication', 'payment', 'shipping', 
        'inventory', 'confirmation', 'returns'
    ]
    
    missing_sections = []
    present_sections = []
    
    for section in required_sections:
        if section in prd or section.replace('_', ' ') in str(prd).lower():
            present_sections.append(section)
        else:
            missing_sections.append(section)
    
    is_valid = len(missing_sections) == 0
    
    return {
        "is_valid": is_valid,
        "present_sections": present_sections,
        "missing_sections": missing_sections,
        "completeness": len(present_sections) / len(required_sections)
    }


def get_tools() -> List[Dict[str, Any]]:
    """
    Get list of available tools for this test case.
    
    Returns:
        List of tool definitions
    """
    return [
        {
            "name": "extract_requirement",
            "description": "Extract structured requirement from text",
            "function": extract_requirement
        },
        {
            "name": "detect_contradiction",
            "description": "Detect if two requirements contradict each other",
            "function": detect_contradiction
        },
        {
            "name": "assess_severity",
            "description": "Assess severity of a contradiction",
            "function": assess_severity
        },
        {
            "name": "generate_clarifying_question",
            "description": "Generate clarifying question for a contradiction",
            "function": generate_clarifying_question
        },
        {
            "name": "validate_prd_structure",
            "description": "Validate PRD has required sections",
            "function": validate_prd_structure
        }
    ]
