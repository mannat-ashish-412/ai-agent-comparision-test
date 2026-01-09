"""
Evaluator for extraction and audit test case.
"""
from typing import Dict, Any


def evaluate(actual_output: Any, expected_output: Dict[str, Any]) -> Dict[str, float]:
    """
    Evaluate the actual output against expected criteria.

    Args:
        actual_output: The actual output from the agent
        expected_output: Expected output structure and criteria

    Returns:
        Dictionary of scores (0-100 for each metric)
    """
    scores = {
        "correctness": 0.0,
        "consistency": 0.0,
        "conflict_handling": 0.0,
        "traceability": 0.0,
    }

    if not isinstance(actual_output, dict):
        return scores

    # Correctness: PRD structure and contradiction detection
    correctness_points = 0

    if "prd" in actual_output:
        correctness_points += 25

        # Check for required sections
        prd = actual_output["prd"]
        required_sections = expected_output["validation_rules"][
            "must_have_prd_sections"
        ]
        prd_str = str(prd).lower()

        sections_found = sum(1 for section in required_sections if section in prd_str)
        correctness_points += (sections_found / len(required_sections)) * 25

    if "contradictions" in actual_output:
        contradictions = actual_output["contradictions"]
        min_expected = expected_output["validation_rules"]["min_contradictions_found"]

        if len(contradictions) >= min_expected:
            correctness_points += 30
        elif len(contradictions) >= min_expected - 2:
            correctness_points += 20
        elif len(contradictions) > 0:
            correctness_points += 10

    if "clarifying_questions" in actual_output:
        questions = actual_output["clarifying_questions"]
        expected_count = expected_output["validation_rules"][
            "clarifying_questions_count"
        ]

        if len(questions) == expected_count:
            correctness_points += 20
        elif len(questions) > 0:
            correctness_points += 10

    scores["correctness"] = min(correctness_points, 100)

    # Consistency: Audit findings match PRD
    consistency_points = 100

    if "contradictions" in actual_output and "prd" in actual_output:
        # Check that contradictions reference items in PRD
        prd_text = str(actual_output["prd"]).lower()
        contradictions = actual_output["contradictions"]

        for contradiction in contradictions:
            # Each contradiction should reference PRD content
            if isinstance(contradiction, dict):
                items = contradiction.get("items", []) or [
                    contradiction.get("req1", ""),
                    contradiction.get("req2", ""),
                ]
                # At least one item should be traceable to PRD
                has_reference = any(
                    any(word in prd_text for word in str(item).lower().split()[:5])
                    for item in items
                    if item
                )
                if not has_reference:
                    consistency_points -= 10

    scores["consistency"] = max(consistency_points, 0)

    # Conflict Handling: Contradictions explicitly flagged
    conflict_points = 0

    if "contradictions" in actual_output:
        contradictions = actual_output["contradictions"]

        if len(contradictions) > 0:
            conflict_points += 40

        # Each contradiction should have details
        detailed_contradictions = 0
        for contradiction in contradictions:
            if isinstance(contradiction, dict):
                has_items = "items" in contradiction or (
                    "req1" in contradiction and "req2" in contradiction
                )
                has_category = "category" in contradiction or "type" in contradiction
                has_severity = "severity" in contradiction

                if has_items and (has_category or has_severity):
                    detailed_contradictions += 1

        if len(contradictions) > 0:
            conflict_points += (detailed_contradictions / len(contradictions)) * 40

    if "resolution_status" in actual_output:
        conflict_points += 20

    scores["conflict_handling"] = conflict_points

    # Traceability: Agent separation visible
    trace_points = 0

    # Check for agent attribution
    output_str = str(actual_output).lower()

    agent_keywords = ["extractor", "auditor", "clarification", "agent"]
    agent_mentions = sum(1 for keyword in agent_keywords if keyword in output_str)

    if agent_mentions >= 2:
        trace_points += 40
    elif agent_mentions >= 1:
        trace_points += 20

    # Check for clear separation of concerns
    has_prd = "prd" in actual_output
    has_contradictions = "contradictions" in actual_output
    has_questions = "clarifying_questions" in actual_output

    if has_prd and has_contradictions:
        trace_points += 30  # Shows extraction and audit separation

    if has_questions:
        trace_points += 30  # Shows clarification generation

    scores["traceability"] = min(trace_points, 100)

    # Pass criteria: All scores ≥ 70, complete PRD, at least 3 contradictions, 3 questions
    scores["passed"] = (
        all(
            score >= 70
            for score in [
                scores["correctness"],
                scores["consistency"],
                scores["conflict_handling"],
            ]
        )
        and len(actual_output.get("contradictions", [])) >= 3
        and len(actual_output.get("clarifying_questions", [])) == 3
        and "prd" in actual_output
    )

    return scores
