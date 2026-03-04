from langgraph.graph import StateGraph, END
from pevr_agent.state import WorkflowState
from pevr_agent.nodes.planner import planner_node
from pevr_agent.nodes.executor import executor_node
from pevr_agent.nodes.verifier import verifier_node


def route(state: WorkflowState):
    """
    Router Logic: Determines the next step based on task status.
    """
    with open("error_log.txt", "a") as f:
        f.write(f"ROUTER: Current Task ID {state.current_task_id}\n")
        if state.plan:
            # Log status of current task
            ct = next((t for t in state.plan if t.id == state.current_task_id), None)
            if ct:
                f.write(f"ROUTER: Status {ct.status}, Retry {ct.retry_count}\n")

    if not state.plan:
        # Should normally have a plan after planner, but if empty, maybe we are done or failed?
        # If we came from planner and it failed to produce a plan, end.
        return END

    # Find current task object
    # If no task ID, we are done (Verifier sets it to None when finished)
    if state.current_task_id is None:
        return END

    current_task = next((t for t in state.plan if t.id == state.current_task_id), None)

    if not current_task:
        return END

    # Analyze current task status
    if current_task.status == "pending":
        return "executor"

    elif current_task.status == "completed":
        # Should have moved to next task in Verifier.
        # If we are here with 'completed', it means Verifier didn't find next?
        # Or Verifier set new task ID, but we retrieved the OLD task using old ID?
        # Wait, Verifier returns updated state. Router sees updated state.
        # So if Verifier set new ID, current_task should be the NEW one (which should be pending).
        # If current_task is still 'completed', it means we are pointing to a completed task.
        # This shouldn't happen if Verifier does its job.
        return END

    elif current_task.status == "failed":
        if current_task.retry_count < state.max_retries:
            # Soft failure, retry
            current_task.retry_count += 1
            return "executor"
        else:
            # Hard failure, re-plan
            return "planner"

    # In progress? execute it
    if current_task.status == "in_progress":
        return "executor"

    return END


def create_pevr_graph():
    """
    Builds the PEVR LangGraph.
    """
    workflow = StateGraph(WorkflowState)

    # Add nodes
    workflow.add_node("planner", planner_node)

    workflow.add_node("executor", executor_node)  # Tools passed via config

    workflow.add_node("verifier", verifier_node)

    # Add edges
    # Planner -> Executor (via router or direct? Router is flexible)
    # We will use conditional edges from Planner to let Router pick the first task

    workflow.set_entry_point("planner")

    workflow.add_conditional_edges("planner", route, {"executor": "executor", END: END})

    workflow.add_edge("executor", "verifier")

    workflow.add_conditional_edges(
        "verifier", route, {"executor": "executor", "planner": "planner", END: END}
    )

    return workflow.compile()
