"""Evaluator for extraction and audit test case using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rules = expected_output.get("validation_rules", {})
    min_contradictions = rules.get("min_contradictions_found", 3)
    expected_questions = rules.get("clarifying_questions_count", 3)
    sections = ", ".join(rules.get("must_have_prd_sections", []))

    rubrics = [
        (
            "correctness",
            f"Evaluate correctness. The output must contain a PRD with sections: {sections}. It must find at least {min_contradictions} contradictions and have {expected_questions} clarifying questions. Score 100 if all met.",
        ),
        (
            "consistency",
            "Evaluate consistency. The found contradictions should accurately reflect items present in the generated PRD. 100 if fully consistent.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. How well are contradictions flagged and detailed (with severity/category)? 100 if details are comprehensive.",
        ),
        (
            "traceability",
            "Evaluate traceability. Does the output show clear separation between extraction, audit, and clarification? 100 if roles are distinct.",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    scores["passed"] = (
        all(
            scores.get(k, 0) >= 70
            for k in ["correctness", "consistency", "conflict_handling"]
        )
        and len(actual_output.get("contradictions", [])) >= min_contradictions
        and len(actual_output.get("clarifying_questions", [])) == expected_questions
        and "prd" in actual_output
    )

    return scores
