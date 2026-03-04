"""Evaluator for parallel document triage test case using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rules = expected_output.get("validation_rules", {})
    unique_items_count = rules.get("unique_items_count", 6)
    expected_dupes = len(expected_output.get("expected_duplicates", []))

    rubrics = [
        (
            "correctness",
            f"Evaluate correctness. The output should have {unique_items_count} unique items in 'processed_items'. Each item must have 'classification' and 'severity'. It should identify and merge approx {expected_dupes} duplicate pairs.",
        ),
        (
            "consistency",
            "Evaluate consistency. Check for duplicate IDs in processed items (should be none). Severity should be consistent with classification (e.g., 'critical' usually for bugs).",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. How well were duplicates identified and merged? Each merged duplicate should have a clear reasoning.",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the 'agent_trace' show multiple distinct agents? Do processed items show which agent handled them?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = (
        all(
            scores.get(k, 0) >= 70
            for k in ["correctness", "consistency", "conflict_handling"]
        )
        and len(actual_output.get("duplicates_merged", [])) >= 4
        and len(actual_output.get("processed_items", [])) == unique_items_count
    )

    return scores
