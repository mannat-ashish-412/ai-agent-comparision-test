import asyncio
import os
from pydantic_evals.evaluators import LLMJudge, EvaluatorContext
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.ollama import OllamaProvider


def _get_judge_model():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    provider = OllamaProvider(base_url=base_url)
    return OpenAIModel("qwen2.5:14b", provider=provider)


async def run_llm_judges(
    actual_output, expected_output, rubrics_with_names, model=None
):
    """
    Run multiple LLM judges on the same output/expected_output pair.

    Args:
        actual_output: The actual output from the agent
        expected_output: The expected output dictionary
        rubrics_with_names: List of (name, rubric) tuples
        model: The model to use for the judge (defaults to qwen2.5:14b via Ollama)

    Returns:
        Dict[str, float]: Dictionary of scores (0-100)
    """
    if model is None:
        model = _get_judge_model()

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
            print(f"{name}: {value_attr}")
            print("-" * 40)
            val = getattr(value_attr, "value", value_attr)

            if isinstance(val, (int, float)):
                f_val = float(val)
                if f_val > 1.0:
                    scores[name] = min(f_val, 100.0)
                else:
                    scores[name] = f_val * 100
            elif isinstance(val, bool):
                scores[name] = 100.0 if val else 0.0
            else:
                scores[name] = 0.0

    return scores