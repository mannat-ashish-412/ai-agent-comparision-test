from pydantic_ai import Agent, Tool
from dotenv import load_dotenv
from test_cases.parallel_doc_triage.mocked_tools import get_tools

load_dotenv()

async def main(system_prompt, user_prompt, tools):
    MODEL = "gpt-4o-mini"

    agent_tools = [
        Tool(**tool) for tool in get_tools()
    ]

    agent = Agent(
        MODEL, system_prompt=system_prompt, user_prompt=user_prompt, tools=agent_tools
    )

    response = await agent.run()
    print(response.output)

if __name__ == "__main__":
    main()
