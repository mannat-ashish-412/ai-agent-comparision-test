from pevr_agent.state import WorkflowState

from langchain_core.runnables import RunnableConfig


async def executor_node(state: WorkflowState, config: RunnableConfig):
    """
    Executor Node: Performs the current task using WorkerAgent.
    """
    with open("error_log.txt", "a") as f:
        f.write(f"EXECUTOR: Task ID {state.current_task_id}\n")

    # Get tools from config
    tools = config.get("configurable", {}).get("tools", [])

    task_id = state.current_task_id
    current_task = next((t for t in state.plan if t.id == task_id), None)

    if not current_task:
        # Should not happen if router logic is correct
        return state

    current_task.status = "in_progress"

    with open("debug_trace.txt", "a") as f:
        f.write(
            f"Executor: Starting task {current_task.id} - {current_task.description}\n"
        )

    # Prepare execution context
    input_data = state.global_context.get("input_data")
    context_str = ""
    if input_data:
        context_str = f"*** INPUT DATA ***\n{input_data}\n*** END INPUT DATA ***\n"
    else:
        context_str = f"Global Context: {state.global_context}"

    prompt = (
        f"Execute Task: {current_task.description}\n\n"
        f"{context_str}\n"
        "INSTRUCTIONS: Use the *** INPUT DATA *** provided above. Do NOT ask for more data.\n"
    )

    if current_task.feedback_log:
        prompt += f"\nPrevious feedback/failure: {current_task.feedback_log[-1]}"

    # Run worker agent with injected tools
    # Note: pydantic-ai agents can accept tools at run time if configured,
    # or we might need to reconstruct the agent.
    # For this implementation, we assume `worker_agent` was initialized without tools
    # and we pass them in `run` if supported, or we rely on a global configuration.
    #
    # Check pydantic_ai docs: agent.run(..., deps=...) or similar.
    # Since `tools` are passed to `Agent` constructor usually, we might need to clone/copy the agent with tools
    # or use a fresh instance in the node if tools are dynamic per request.
    #
    # Given the constraint of 'main.py' passing tools, we will create a temporary agent instance here
    # or use the one from `agents.py` if we can assume tools are set globally?
    # Actually, `pydantic_ai` allows passing `deps` but tools are usually static to the agent definition
    # OR dynamic via context.
    #
    # Workaround: We will use the `deps` to pass tools? No, tools are functions.
    # Let's try to construct a new agent instance here for now to support dynamic tools from main.py

    from pydantic_ai import Agent
    from pydantic_ai.providers.ollama import OllamaProvider
    from pydantic_ai.models.openai import OpenAIModel
    import os

    _base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    _model = OpenAIModel("qwen2.5:14b", provider=OllamaProvider(base_url=_base_url))

    runtime_worker = Agent(
        _model,
        system_prompt=(
            "You are a skilled developer worker. Your goal is to execute the assigned task "
            "using the available tools. You should produce a result summary. "
            "Focus ONLY on the current task. Do not try to do more than what is asked."
            "CRITICAL: The input data you need (e.g., issues, documents) is available in 'Global Context'. "
            "You MUST use this data to complete the task. Do NOT ask the user for it. "
            "Do NOT provide a template or plan. Provide the ACTUAL COMPLETED OUTPUT using the context data."
        ),
        tools=tools,
    )

    result = await runtime_worker.run(prompt)

    # Store result
    # We output the raw result text representation
    current_task.result_summary = str(result.output)

    return state