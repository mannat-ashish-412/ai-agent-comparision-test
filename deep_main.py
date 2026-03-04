import traceback
import asyncio
import json
from langchain_ollama import ChatOllama
from langchain_core.tools import StructuredTool
from deepagents import create_deep_agent
from dotenv import load_dotenv
from test_cases.test_runner import run_test, run_tests
import os

load_dotenv()

llm = ChatOllama(
    model="qwen2.5:14b",
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434").replace("/v1", ""),
    temperature=0,
    num_ctx=8192,
)


def _convert_tools(tools: list) -> list:
    """
    Convert test_runner tool dicts (name, description, function)
    into LangChain StructuredTool objects that deepagents can use.
    """
    return [
        StructuredTool.from_function(
            func=t["function"],
            name=t["name"],
            description=t["description"],
        )
        for t in tools
    ]


async def main(system_prompt: str, user_prompt: str, tools: list, output_type):
    try:
        lc_tools = _convert_tools(tools)

        agent = create_deep_agent(
            model=llm,
            tools=lc_tools,
            system_prompt=system_prompt,
            response_format=output_type,
        )

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_prompt}]
        })

        # deepagents returns the structured output in result["structured_response"]
        # or the last message — try both
        if isinstance(result, dict):
            if "structured_response" in result:
                return result["structured_response"]
            # fallback: last message content
            messages = result.get("messages", [])
            if messages:
                return messages[-1].content
        return result

    except Exception as e:
        print(traceback.format_exc())
        print("Error: ", e)
        return None


async def check_agent():
    result = await run_test("entraid_roles_update", main)
    # result = await run_test("pagination_evacuation", main)
    # result = await run_test("safe_ops_approval", main)
    # results = await run_tests(main)
    with open("test_results_deepagent.json", "w") as f:
        json.dump({"result": str(result)}, f, indent=4)
    return result


if __name__ == "__main__":
    asyncio.run(check_agent())