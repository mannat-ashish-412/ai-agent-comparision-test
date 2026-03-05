import asyncio
import os
import json
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic import BaseModel


class JudgeResult(BaseModel):
    passed: bool
    score: float  # 0.0 to 100.0
    reason: str


def _get_judge_model():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    provider = OllamaProvider(base_url=base_url)
    return OpenAIModel("qwen2.5:14b", provider=provider)


async def _run_single_judge(name: str, rubric: str, actual_output, expected_output, model) -> tuple[str, float]:
    agent = Agent(
        model,
        system_prompt=(
            "You are an evaluation judge. Given a rubric, actual output, and expected output, "
            "score the actual output. Return whether it passed and a score from 0-100."
        ),
        output_type=JudgeResult,
        retries=2,
    )

    prompt = (
        f"Rubric: {rubric}\n\n"
        f"Expected Output: {json.dumps(expected_output)}\n\n"
        f"Actual Output: {json.dumps(actual_output)}\n\n"
        "Evaluate whether the actual output satisfies the rubric."
    )

    try:
        result = await agent.run(prompt)
        jr = result.output
        print(f"{name}: {jr}")
        print("-" * 40)
        return name, jr.score
    except Exception as e:
        print(f"{name}: evaluation failed - {e}")
        print("-" * 40)
        return name, 0.0


async def run_llm_judges(
    actual_output, expected_output, rubrics_with_names, model=None
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
    if model is None:
        model = _get_judge_model()

    tasks = [
        _run_single_judge(name, rubric, actual_output, expected_output, model)
        for name, rubric in rubrics_with_names
    ]

    results = await asyncio.gather(*tasks)
    return dict(results)