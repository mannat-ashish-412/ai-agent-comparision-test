import asyncio
import traceback
from dotenv import load_dotenv
from pevr_agent.workflow import create_pevr_graph
from pevr_agent.state import WorkflowState
from test_cases.test_runner import run_test
import json

load_dotenv()


async def main(system_prompt, user_prompt, tools, output_type):
    """
    Adapter function that matches the signature expected by test_runner.
    """
    try:
        # agent_tools = [Tool(**tool, max_retries=3) for tool in tools]

        # Initialize Graph
        graph = create_pevr_graph()

        initial_state = WorkflowState(user_goal=user_prompt)

        # Run Graph
        final_state = await graph.ainvoke(initial_state, config={})

        print(final_state)
    except Exception:
        print(traceback.format_exc())
        return None


async def check_pevr_agent():
    result = await run_test("pagination_evacuation", main)
    # result = await run_test("safe_ops_approval", main)
    # result = await run_tests(main)
    with open("test_results.json", "w") as f:
        json.dump({"result": result}, f, indent=4)
    return result


if __name__ == "__main__":
    asyncio.run(check_pevr_agent())
