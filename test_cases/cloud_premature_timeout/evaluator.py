"""Evaluator for Cloud Premature Timeout test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. Did the table get created successfully? Look for 'Success: Table users created'.",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent avoid calling 'create_db' more than once?",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Did the agent use the 'wait' tool and check status in a loop until it was AVAILABLE?",
        ),
        (
            "traceability",
            "Evaluate traceability. Did the logs show the waiting process?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Heuristic checks
    output_str = str(actual_output)
    success = "Success: Table 'users' created" in output_str

    scores["passed"] = scores.get("correctness", 0) >= 80 and success

    return scores
