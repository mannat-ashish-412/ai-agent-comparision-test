import asyncio
from pydantic_evals.evaluators import LLMJudge, EvaluatorContext


async def run_llm_judges(
    actual_output, expected_output, rubrics_with_names, model="ollama:qwen2.5:14b"
):
    """
    Run multiple LLM judges on the same output/expected_output pair.

    Args:
        actual_output: The actual output from the agent
        expected_output: The expected output dictionary
        rubrics_with_names: List of (name, rubric) tuples
        model: The model to use for the judge

    Returns:
        Dict[str, float]: Dictionary of scores (0-100)
    """
    judges = [
        LLMJudge(rubric=rubric, score={"evaluation_name": name}, model=model)
        for name, rubric in rubrics_with_names
    ]

    ctx = EvaluatorContext(
        name="test_case_eval",
        inputs=None,
        metadata=None,
        expected_output=expected_output,
        output=actual_output,
        duration=0.0,
        _span_tree=None,
        attributes={},
        metrics={},
    )

    results = await asyncio.gather(*[j.evaluate(ctx) for j in judges])

    scores = {}
    for result in results:
        for name, value_attr in result.items():
            # LLMJudge might return a dictionary of numeric scores (dict[str, float])
            # or a dictionary of EvaluationReason objects (dict[str, EvaluationReason])
            print(f"{name}: {value_attr}")
            print("-" * 40)
            val = getattr(value_attr, "value", value_attr)

            if isinstance(val, (int, float)):
                f_val = float(val)
                # Some models return 0-100, others return 0-1
                if f_val > 1.0:
                    scores[name] = min(f_val, 100.0)
                else:
                    scores[name] = f_val * 100
            elif isinstance(val, bool):
                scores[name] = 100.0 if val else 0.0
            else:
                scores[name] = 0.0

    return scores
