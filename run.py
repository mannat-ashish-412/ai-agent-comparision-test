import asyncio
import traceback
from dotenv import load_dotenv
from pevr_agent.workflow import create_pevr_graph
from pevr_agent.state import WorkflowState
from test_cases.test_runner import run_test
from pydantic_ai import Tool
import json
from pathlib import Path

load_dotenv()


# Global to store input data for current test run
TEST_INPUT_DATA = None


async def main(system_prompt, user_prompt, tools, output_type):
    """
    Adapter function that matches the signature expected by test_runner.
    """
    try:
        # Convert dict tools to pydantic_ai Tool objects if they aren't already
        # test_runner passes a list of tool definitions (dicts) or Tool objects?
        # looking at main.py: agent_tools = [Tool(**tool, max_retries=3) for tool in tools]
        # So 'tools' is a list of dicts.

        agent_tools = [Tool(**tool, max_retries=3) for tool in tools]

        # Initialize Graph
        graph = create_pevr_graph()

        # Initialize State
        # Load input data from global if available (hack for test runner constraint)
        global TEST_INPUT_DATA
        context = {}
        if TEST_INPUT_DATA:
            context["input_data"] = TEST_INPUT_DATA

        initial_state = WorkflowState(user_goal=user_prompt, global_context=context)

        # Run Graph
        # Pass tools via configurable config
        config = {"recursion_limit": 150, "configurable": {"tools": agent_tools}}
        final_state = await graph.ainvoke(initial_state, config=config)

        # Extract Result
        # The test runner expects the result to match 'output_type' schema.
        # But PEVR returns a final state. We need to parse the last result into 'output_type'.
        # Or, if output_type is Pydantic model, we try to parse the text.

        # For now, let's assume the last completed task contains the final answer JSON.
        # We need a robust way to get the final answer.
        # We can look for a task named "Final Answer" or just take the last result.

        if not final_state["plan"]:
            return None

        # Get result from the last task (which ideally is the final answer)
        # We need to make sure the Architect plans a final answer task.
        # For robustness, we'll try to parse the last task's result.

        last_task_result = final_state["plan"][-1].result_summary

        # If output_type is a Pydantic model, we assume the result string is JSON
        if output_type:
            # Basic attempt to parse JSON from string if it's not a pure string
            try:
                # If result is already a dict (unlikely from str), good.
                # If it's a string, try loading it.
                if isinstance(last_task_result, str):
                    # Clean up code blocks if present
                    clean_result = last_task_result.strip()
                    if clean_result.startswith("```json"):
                        clean_result = clean_result[7:]
                    if clean_result.startswith("```"):
                        clean_result = clean_result.strip("`")
                    if clean_result.endswith("```"):
                        clean_result = clean_result[:-3]

                    data = json.loads(clean_result)
                    return output_type(**data)
            except Exception as e:
                print(f"Failed to parse output as {output_type}: {e}")
                # Fallback: return raw string if it was just a string
                return last_task_result

        return last_task_result

    except Exception:
        with open("error_log.txt", "a") as f:
            f.write("\n" + traceback.format_exc())
        print("Error occurred. See error_log.txt for details.")
        return None


async def run_pevr_tests():
    # Run single test case as requested
    print("Running Verification: 'parallel_doc_triage'...")
    result = await run_test("parallel_doc_triage", main)
    print(f"Result: {result}")


if __name__ == "__main__":
    # Load input data for parallel_doc_triage manually since test_runner doesn't pass it
    try:
        data_path = Path("test_cases/parallel_doc_triage/input_data.json")
        if data_path.exists():
            with open(data_path) as f:
                TEST_INPUT_DATA = json.load(f)
    except Exception as e:
        print(f"Failed to load input data: {e}")

    # Run the test
    asyncio.run(run_pevr_tests())
