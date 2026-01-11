"""Evaluator for tool conflict resolution test case using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    valid_policies = expected_output.get("valid_resolution_policies", [])

    rubrics = [
        (
            "correctness",
            f"Evaluate correctness. The agent must detect conflicts between sources. It must choose a resolution policy from: {', '.join(valid_policies)}. The 'final_price' must be either 999 or 1099.",
        ),
        (
            "consistency",
            "Evaluate consistency. The 'final_price' choice must align with the stated 'resolution_policy'. For example, if policy is 'api_priority', price should match API value.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Are 'detected_conflicts' detailed with sources and values? Is the 'resolution_policy' explicit?",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the 'audit_trail' mention specific sources (api, catalog, etc.) and explain WHY a choice was made?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = all(
        scores.get(k, 0) >= 70
        for k in ["correctness", "consistency", "conflict_handling", "traceability"]
    )

    return scores
