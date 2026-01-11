"""Evaluator for RCA test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. The output must have 'root_cause', 'proposed_patch', and at least 2 'regression_tests'. Root cause should correctly identify the precision issue (the '+' character in logging).",
        ),
        (
            "consistency",
            "Evaluate consistency. The proposed patch should directly address the identified root cause. Regression tests should specifically target the failure scenario.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. How well did the agent handle the discrepancy between log output and code logic?",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the RCA explain how it arrived at the root cause from the provided logs?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = (
        all(
            scores.get(k, 0) >= 70
            for k in ["correctness", "consistency", "conflict_handling"]
        )
        and "root_cause" in actual_output
        and "proposed_patch" in actual_output
        and len(actual_output.get("regression_tests", [])) >= 2
    )

    return scores
