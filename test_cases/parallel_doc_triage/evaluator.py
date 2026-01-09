"""
Evaluator for parallel document triage test case.
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

    # Correctness: Check structure and classifications
    correctness_points = 0
    max_correctness = 100

    # Check required fields
    if "processed_items" in actual_output:
        correctness_points += 20
        items = actual_output["processed_items"]

        # Check unique items count
        expected_count = expected_output["validation_rules"]["unique_items_count"]
        if len(items) == expected_count:
            correctness_points += 20
        elif abs(len(items) - expected_count) <= 1:
            correctness_points += 10

        # Check classifications
        correct_classifications = 0
        total_items = len(items)
        for item in items:
            if "classification" in item and "severity" in item:
                correct_classifications += 1

        if total_items > 0:
            correctness_points += (correct_classifications / total_items) * 30

    if "duplicates_merged" in actual_output:
        correctness_points += 15

        # Check if expected duplicates were identified
        expected_dupes = len(expected_output["expected_duplicates"])
        actual_dupes = len(actual_output["duplicates_merged"])
        if actual_dupes >= expected_dupes - 1:
            correctness_points += 15

    scores["correctness"] = min(correctness_points, max_correctness)

    # Consistency: Check for contradictions
    consistency_points = 100

    if "processed_items" in actual_output:
        items = actual_output["processed_items"]

        # Check for duplicate IDs
        ids = [item.get("id") for item in items if "id" in item]
        if len(ids) != len(set(ids)):
            consistency_points -= 30

        # Check severity consistency with classification
        for item in items:
            classification = item.get("classification")
            severity = item.get("severity")

            # Critical severity should only be for bugs
            if severity == "critical" and classification != "bug":
                consistency_points -= 20

    scores["consistency"] = max(consistency_points, 0)

    # Conflict Handling: Check deduplication quality
    conflict_points = 0

    if "duplicates_merged" in actual_output:
        duplicates = actual_output["duplicates_merged"]

        # Should have identified duplicates
        if len(duplicates) > 0:
            conflict_points += 40

        # Each duplicate should have reasoning
        has_reasoning = sum(
            1 for dup in duplicates if "reason" in dup or "reasoning" in dup
        )
        if len(duplicates) > 0:
            conflict_points += (has_reasoning / len(duplicates)) * 60

    scores["conflict_handling"] = conflict_points

    # Traceability: Check agent trace
    trace_points = 0

    if "agent_trace" in actual_output:
        trace_points += 40

        trace = actual_output["agent_trace"]

        # Should have multiple agents mentioned
        if isinstance(trace, dict):
            agent_count = len(trace)
            if agent_count >= 3:
                trace_points += 30
            elif agent_count >= 2:
                trace_points += 15

        # Items should reference which agent processed them
        if "processed_items" in actual_output:
            items_with_agent = sum(
                1
                for item in actual_output["processed_items"]
                if "processed_by_agent" in item or "agent" in item
            )
            total_items = len(actual_output["processed_items"])
            if total_items > 0:
                trace_points += (items_with_agent / total_items) * 30

    scores["traceability"] = trace_points

    # Pass criteria: All scores ≥ 70, 4 duplicate pairs, 6 unique items
    scores["passed"] = (
        all(
            score >= 70
            for score in [
                scores["correctness"],
                scores["consistency"],
                scores["conflict_handling"],
            ]
        )
        and len(actual_output.get("duplicates_merged", [])) >= 4
        and len(actual_output.get("processed_items", [])) == 6
    )

    return scores
