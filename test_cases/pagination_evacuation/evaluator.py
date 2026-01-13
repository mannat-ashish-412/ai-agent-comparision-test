"""Evaluator for pagination evacuation test using LLMJudge."""
from typing import Any, Dict
import json
from pathlib import Path
from eval_utils import run_llm_judges


async def evaluate(
    actual_output: Dict[str, Any], expected_output: Dict[str, Any]
) -> Dict[str, Any]:
    # 1. Load Ground Truth (Simulated DB)
    db_path = Path(__file__).parent / "simulated_db.json"
    real_evacuated_users = []
    if db_path.exists():
        with open(db_path, "r") as f:
            try:
                real_evacuated_users = json.load(f)
            except json.JSONDecodeError:
                pass

    # 2. Get Input Data (to know what should have been done)
    # Assuming we know expected total users. For stricter diff, we load the input file.
    input_path = Path(__file__).parent / "input_data.json"
    with open(input_path) as f:
        input_data = json.load(f)
        all_expected_ids = [u["id"] for u in input_data["users"]]

    # 3. Get Agent Claims
    claimed_ids = actual_output.get("processed_user_ids", [])

    # 4. Calculate Diffs
    real_set = set(real_evacuated_users)
    expected_set = set(all_expected_ids)
    claimed_set = set(claimed_ids)

    missed_users = list(expected_set - real_set)
    hallucinated_claims = list(
        claimed_set - real_set
    )  # Claimed processing but didn't actually write to DB

    real_count = len(real_set)
    total_count = len(expected_set)
    success = real_count == total_count

    # 5. Construct Detailed Rubrics with Static Data
    rubrics = [
        (
            "correctness",
            f"Evaluate correctness. The agent processed {real_count}/{total_count} users. \n"
            f"Missed Users: {missed_users}\n"
            f"Hallucinated Claims (Claimed but not in DB): {hallucinated_claims}\n"
            "If missed_users is empty AND hallucinated_claims is empty, score 100%. Otherwise score 0%.",
        ),
        (
            "consistency",
            f"Evaluate consistency. The agent matched {len(claimed_set & real_set)} valid records. \n"
            f"Did the agent claim to process users it actually didn't? (Hallucinations: {len(hallucinated_claims)})",
        ),
        (
            "conflict_handling",
            "Evaluate conflict handling. Did the agent persist effectively through pagination?",
        ),
        (
            "traceability",
            f"Evaluate traceability. The final output list contains {len(claimed_ids)} items. Does this match the actual specific IDs processed?",
        ),
    ]

    scores = await run_llm_judges(actual_output, expected_output, rubrics)

    # Hard override for correctness
    scores["correctness"] = (
        100.0
        if success and not hallucinated_claims
        else (real_count / total_count * 100)
    )
    scores["passed"] = success

    return scores
