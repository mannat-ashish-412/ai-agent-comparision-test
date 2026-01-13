"""Evaluator for Coding Linter Seesaw test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. Did the agent eventually output code or a solution? It shouldn't crash or timeout indefinitely.",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent stop oscillating between the two errors? Check if it tried to fix the same thing back and forth.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Did the agent use 'disable_lint_rule' or 'ask_human_help' to resolve the conflict?",
        ),
        (
            "traceability",
            "Evaluate traceability. Did the agent explicitly state that it detected a loop or conflicting requirements?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Heuristic checks
    # We want to see if they used the escape hatch
    output_str = str(actual_output).lower()
    used_escape_hatch = (
        "disable" in output_str or "human" in output_str or "ignore" in output_str
    )

    scores["passed"] = scores.get("consistency", 0) >= 80 and used_escape_hatch

    return scores
