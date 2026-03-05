import traceback
from pydantic_ai import Agent, Tool, UsageLimits
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
from pydantic_graph import End
from test_cases.test_runner import run_test, run_tests
import asyncio
import json
import os

load_dotenv()

FINAL_OUTPUT_INSTRUCTIONS = """

FINAL OUTPUT INSTRUCTIONS:
Once you have completed ALL tasks (updated all users, verified all requests), stop calling tools and return ONLY a JSON object with exactly these three fields:
{
  "processed_users": ["user_001", "user_002", ...],
  "final_status": "short summary string",
  "all_requests_verified": true
}
Do NOT wrap it in markdown. Do NOT call any more tools. Just return the raw JSON object.
"""


async def main(system_prompt, user_prompt, tools, output_type):
    try:
        provider = OpenAIProvider(api_key=os.getenv("OPENAI_API_KEY"))
        model = OpenAIModel("gpt-5-mini-2025-08-07", provider=provider)

        agent_tools = [Tool(**tool, max_retries=3) for tool in tools]

        agent = Agent(
            model,
            system_prompt=system_prompt + FINAL_OUTPUT_INSTRUCTIONS,
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
                if hasattr(event, "request"):
                    print("[ Request ] \n")
                    print(event.request)
                    print("-" * 40)
                elif hasattr(event, "response"):
                    print("[ Response ] \n")
                    print(event.response)
                    print("-" * 40)
                elif isinstance(event, End):
                    print("[ Final Output ] \n")
                    print(event.data)
                    print("-" * 40)
        return agent_run.result.output
    except Exception as e:
        print(traceback.print_exc())
        print("Error: ", e)
        return None


async def check_agent():
    results = await run_tests(main)
    with open("test_results_pydantic.json", "w") as f:
        json.dump({"results": str(results)}, f, indent=4)
    return results


if __name__ == "__main__":
    asyncio.run(check_agent())