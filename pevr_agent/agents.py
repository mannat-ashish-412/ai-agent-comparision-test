from pydantic_ai import Agent
from pydantic_ai.providers.ollama import OllamaProvider
from pydantic_ai.models.openai import OpenAIModel
from pevr_agent.state import Task
from typing import List
from pydantic import BaseModel
import os


def get_model():
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    provider = OllamaProvider(base_url=base_url)
    return OpenAIModel("qwen2.5:14b", provider=provider)


class Plan(BaseModel):
    tasks: List[Task]


# Architect Agent: Breaks down goals into tasks
architect_agent = Agent(
    get_model(),
    system_prompt=(
        "You are an expert software architect. Your goal is to break down a complex user request "
        "into a dependency graph of small, isolated, executable tasks. "
        "Each task should have a clear description and dependencies if any. "
        "Return the plan as a list of Task objects. "
        "Ensure the tasks allow for incremental progress and are verifiable."
    ),
    output_type=Plan,
)

# Worker Agent: Executes a single task
worker_agent = Agent(
    get_model(),
    system_prompt=(
        "You are a skilled developer worker. Your goal is to execute the assigned task "
        "using the available tools. You should produce a result summary. "
        "Focus ONLY on the current task. Do not try to do more than what is asked."
    ),
)


# Critic Agent: Verifies the result
class VerificationResult(BaseModel):
    is_valid: bool
    critique: str


critic_agent = Agent(
    get_model(),
    system_prompt=(
        "You are a critical QA engineer. Your goal is to verify the output of a task "
        "against its description. check for correctness, completeness, and adherence to requirements. "
        "If the result is flawed, provide a specific critique. "
        "Be strict but fair."
    ),
    output_type=VerificationResult,
)