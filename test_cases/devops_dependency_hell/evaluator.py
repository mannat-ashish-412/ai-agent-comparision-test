"""Evaluator for DevOps Dependency Hell test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. Did the agent end up with BOTH requests==2.0 and authlib==2.0? If it reverted to 1.0, that is a fail.",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent avoid an infinite install/revert loop?",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Did the agent interpret the error message 'authlib 1.0 is incompatible' correctly and chose to update authlib?",
        ),
        (
            "traceability",
            "Evaluate traceability. Did the agent identify the root cause as a dependency mismatch?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Heuristic checks
    # Since we can't easily check the final state of the mock in the evaluator without passing it through,
    # we rely on the agent's final report or if the 'mocked_tools' state was somehow exposed (it isn't here easily).
    # We will rely on text output confirmation.

    output_str = str(actual_output)
    success = "authlib==2.0" in output_str and "requests==2.0" in output_str

    scores["passed"] = scores.get("correctness", 0) >= 80 and success

    return scores
