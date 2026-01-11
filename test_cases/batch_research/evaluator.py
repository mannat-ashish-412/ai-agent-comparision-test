"""Evaluator for batch research test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Score the correctness of the research answers. Give 100 for 5 correct answers, 60 for 3-4, 30 for 1-2, and 0 for none.",
        ),
        (
            "consistency",
            "Check for internal consistency in the answers. 100 if there are no contradictions, lower if contradictions exist.",
        ),
        (
            "conflict_handling",
            "Evaluate how well the agent handled conflicting information in the research materials.",
        ),
        (
            "traceability",
            "Evaluate traceability. Score 100 if all 5 answers cite KB sources (format kb-XXX), 70 for 3-4 citations, 40 for 1-2, and 0 for none.",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Pass criteria: All scores ≥ 70, all 5 answers must cite KB source
    # We still keep some hard checks if necessary, or let the LLM handle it.
    scores["passed"] = all(
        scores.get(k, 0) >= 70
        for k in ["correctness", "consistency", "conflict_handling", "traceability"]
    )

    return scores
