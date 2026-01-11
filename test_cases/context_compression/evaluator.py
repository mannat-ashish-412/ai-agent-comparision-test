"""Evaluator for context compression test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Score the correctness of the final answer. It MUST mention RDS and the specific instance type 'db.t3.medium'. 100 if both are present and correct, 50 if only one is present, 0 otherwise.",
        ),
        (
            "consistency",
            "Check for consistency. The agent should recommend RDS and NOT self-managed PostgreSQL. 100 if consistent with RDS recommendation, lower if self-managed is mentioned as a viable alternative.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. The agent had to choose between multiple database options. 100 if it correctly chose RDS based on requirements, 0 otherwise.",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the response show evidence of analyzing the source documents? 100 if sources are cited or compressed state shows clear analysis.",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    answer_text = str(actual_output.get("final_answer", "")).lower()
    scores["passed"] = (
        all(
            scores.get(k, 0) >= 70
            for k in ["correctness", "consistency", "conflict_handling", "traceability"]
        )
        and "rds" in answer_text
        and "self-managed" not in answer_text
    )

    return scores
