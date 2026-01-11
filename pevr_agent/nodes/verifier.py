from pevr_agent.state import WorkflowState
from pevr_agent.agents import critic_agent


async def verifier_node(state: WorkflowState):
    """
    Verifier Node: Critiques the output of the Executor.
    """
    with open("error_log.txt", "a") as f:
        f.write(f"VERIFIER: Task ID {state.current_task_id}\n")

    task_id = state.current_task_id
    current_task = next((t for t in state.plan if t.id == task_id), None)

    if not current_task or not current_task.result_summary:
        return state

    with open("debug_trace.txt", "a") as f:
        f.write(f"Verifier: Checking task {current_task.id}\n")

    prompt = (
        f"Task Description: {current_task.description}\n"
        f"Task Result: {current_task.result_summary}\n"
        "Verify if the result meets the task requirements."
    )

    result = await critic_agent.run(prompt)
    verification = result.output  # VerificationResult

    with open("error_log.txt", "a") as f:
        f.write(f"VERIFICATION RESULT: {verification.is_valid}\n")
        f.write(f"CRITIQUE: {verification.critique}\n")

    # Update task status based on verification
    if verification.is_valid:
        current_task.status = "completed"
        current_task.feedback_log.append(
            "Verification Passed: " + verification.critique
        )

        # Select next task
        next_task = next((t for t in state.plan if t.status == "pending"), None)
        if next_task:
            state.current_task_id = next_task.id
        else:
            state.current_task_id = None  # No more tasks

    else:
        current_task.status = "failed"
        current_task.feedback_log.append(
            "Verification Failed: " + verification.critique
        )
        # Keep current_task_id to allow retry or replan logic in Router to see it

    return state
