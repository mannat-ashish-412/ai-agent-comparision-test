import traceback
from pydantic_ai import Agent, Tool, UsageLimits
from dotenv import load_dotenv
from test_cases.test_runner import run_test
import asyncio
import json

load_dotenv()


async def main(system_prompt, user_prompt, tools, output_type):
    try:
        MODEL = "gpt-4o-mini"

        agent_tools = [Tool(**tool, max_retries=3) for tool in tools]

        agent = Agent(
            MODEL,
            system_prompt=system_prompt,
            tools=agent_tools,
            output_type=output_type,
            output_retries=3,
            retries=3,
        )

        async with agent.iter(
            user_prompt,
            usage_limits=UsageLimits(request_limit=50),
        ) as agent_run:
            async for event in agent_run:
                print("[ EVENT ] \n")
                print(event)
                print("-" * 40)
                pass

        return agent_run.result.output
    except Exception as e:
        print(traceback.print_exc())
        print("Error: ", e)
        return None


async def check_agent():
    result = await run_test("entraid_roles_update", main)
    # result = await run_test("pagination_evacuation", main)
    # result = await run_test("safe_ops_approval", main)
    # result = await run_tests(main)
    with open("test_results.json", "w") as f:
        json.dump({"result": result}, f, indent=4)
    return result


if __name__ == "__main__":
    asyncio.run(check_agent())
