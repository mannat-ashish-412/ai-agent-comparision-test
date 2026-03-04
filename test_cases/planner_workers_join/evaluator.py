"""Evaluator for planner-workers-join test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. The output must have a 'unified_plan' and 'findings_by_area' covering: data_modeling, access_patterns, and migration_steps. 100 if all areas are covered with quality findings.",
        ),
        (
            "consistency",
            "Evaluate consistency. Check the 'consistency_check' field. It should accurately reflect if the sub-plans align with the unified strategy.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Is the 'unified_plan' substantive and does it resolve potential overlaps between the three areas?",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the unified plan clearly reference the findings from the different areas?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = (
        all(
            scores.get(k, 0) >= 70
            for k in ["correctness", "consistency", "conflict_handling"]
        )
        and "unified_plan" in actual_output
        and len(actual_output.get("findings_by_area", {})) >= 3
    )

    return scores
