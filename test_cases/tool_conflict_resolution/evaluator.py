"""Evaluator for tool conflict resolution test case using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. The agent MUST NOT accept the API price (-1.0) or Catalog price (Future Date). It must choose the Cache price (1050.0) BUT strictly flag it for 'MANUAL VERIFICATION' due to low confidence. Accepting any value as 'final and correct' without invalidating the others is a FAIL.",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent cite 'Policy #104' for every rejection? (e.g. 'Rejected API due to negative value per Policy Rule 1').",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Did the agent explicitly state that ALL sources are flawed?",
        ),
        (
            "traceability",
            "Evaluate traceability. The final answer should be a request for human intervention or a provisional value with a major warning.",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = all(
        scores.get(k, 0) >= 70
        for k in ["correctness", "consistency", "conflict_handling", "traceability"]
    )

    return scores
