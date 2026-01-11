from pevr_agent.state import WorkflowState
from pevr_agent.agents import architect_agent


async def planner_node(state: WorkflowState):
    """
    Planner Node: Uses ArchitectAgent to create or refine the plan.
    """
    # Prepare prompt based on whether it's an initial plan or a replan
    if not state.plan:
        prompt = f"Create a plan for the user goal: {state.user_goal}"
    else:
        # Re-planning scenario: provide context on failures
        failed_tasks = [t for t in state.plan if t.status == "failed"]
        feedback = "\n".join(
            [
                f"Task '{t.description}' failed: {t.feedback_log[-1]}"
                for t in failed_tasks
            ]
        )
        prompt = (
            f"The previous plan failed. Re-plan to achieve the goal: {state.user_goal}\n"
            f"Failures:\n{feedback}\n"
            "Update the plan by adding alternative tasks or breaking down the failed steps."
        )

    # Run the architect agent
    result = await architect_agent.run(prompt)

    state.plan = result.output.tasks

    # Initialize first task
    if state.plan:
        state.current_task_id = state.plan[0].id

    return state
