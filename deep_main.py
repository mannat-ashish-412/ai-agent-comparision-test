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


def _extract_structured_output(content: str, output_type):
    """
    Parse the agent's final text response into the required Pydantic output type.
    Uses the LLM to extract structured JSON if direct parsing fails.
    """
    # Try direct JSON parse first
    try:
        # strip markdown code fences if present
        cleaned = content.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]
            if cleaned.startswith("json"):
                cleaned = cleaned[4:]
        return output_type.model_validate_json(cleaned.strip())
    except Exception:
        pass

    # Fallback: ask the LLM to reformat the response as JSON
    try:
        schema = output_type.model_json_schema()
        prompt = (
            f"Extract the following information from the text below and return ONLY a valid JSON object "
            f"matching this schema: {json.dumps(schema)}\n\n"
            f"Text:\n{content}\n\n"
            f"Return ONLY the raw JSON object, no markdown, no explanation."
        )
        response = llm.invoke(prompt)
        raw = response.content.strip()
        if raw.startswith("```"):
            raw = raw.split("```")[1]
            if raw.startswith("json"):
                raw = raw[4:]
        return output_type.model_validate_json(raw.strip())
    except Exception as e:
        print(f"Structured output extraction failed: {e}")
        return None


async def main(system_prompt: str, user_prompt: str, tools: list, output_type):
    try:
        lc_tools = _convert_tools(tools)

        agent = create_deep_agent(
            model=llm,
            tools=lc_tools,
            system_prompt=system_prompt,
        )

        result = await agent.ainvoke({
            "messages": [{"role": "user", "content": user_prompt}]
        })

        # Extract final message content
        messages = result.get("messages", [])
        if not messages:
            print("No messages in result")
            return None

        last_message = messages[-1]
        content = last_message.content if hasattr(last_message, "content") else str(last_message)

        print("\n[ Deep Agent Final Response ]\n")
        print(content)
        print("-" * 40)

        # Parse into structured output
        return _extract_structured_output(content, output_type)

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