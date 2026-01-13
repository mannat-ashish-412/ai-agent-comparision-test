"""Evaluator for App Security Blind Patcher test using LLMJudge."""
from typing import Dict, Any
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Any, expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    rubrics = [
        (
            "correctness",
            "Evaluate correctness. Did the agent use a proper HTML sanitization library (e.g., 'bleach', 'html.escape')? Deduct points if it used regex or manual string replacement. 100 if a library is used.",
        ),
        (
            "consistency",
            "Evaluate consistency. Did the agent explicitly test with 'polyglot' payloads using verify_security? It should not just rely on 'standard'.",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. N/A for this test, give 100.",
        ),
        (
            "traceability",
            "Evaluate traceability. Did the logs or output show an explicit 'Attack' or 'Red Team' step where it tried to break its own code?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Heuristic checks
    code_content = actual_output.get("code", "")

    # Check if 'polyglot' was used in tool calls (this would ideally be checked against execution logs,
    # but here we rely on the LLM judge or if the agent output mentions it)
    # For a stricter check, we'd need access to the tool call history.
    # We will rely on the code content showing imports for sanitization.

    uses_library = any(
        lib in code_content for lib in ["bleach", "html.escape", "markupsafe"]
    )

    scores["passed"] = (
        scores.get("correctness", 0) >= 80
        and scores.get("consistency", 0) >= 70
        and uses_library
    )

    return scores
