"""
Simple example script demonstrating the agent system usage.
"""

import asyncio
from pathlib import Path

from langgraph_pydantic_agent import run_agent
from config import get_settings, update_settings
from utils import save_state_to_file, get_task_statistics, format_execution_summary
from logger import get_logger

logger = get_logger(__name__)


async def example_basic():
    """Basic usage example."""
    print("\n" + "=" * 60)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 60 + "\n")

    result = await run_agent(
        user_request="Create a simple Python calculator that can add, subtract, multiply, and divide numbers",
        system_prompt="You are a helpful Python programming assistant.",
    )

    # Print summary
    print(result.get("final_summary", "No summary available"))

    # Save results
    filepath = save_state_to_file(result)
    print(f"\n💾 Results saved to: {filepath}")


async def example_custom_models():
    """Example with custom model configuration."""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Custom Model Configuration")
    print("=" * 60 + "\n")

    # Configure different models for different agents
    settings = update_settings(
        default_model="openai:gpt-4o",
        agent_models={
            "planning": "openai:gpt-4o",
            "decomposition": "openai:gpt-4o",
            "execution": "openai:gpt-4o",
            "verification": "openai:gpt-4o-mini",  # Use cheaper model for verification
            "final_verification": "openai:gpt-4o",
        },
    )

    result = await run_agent(
        user_request="Analyze a dataset: load CSV, clean data, perform statistical analysis, and create visualizations",
        system_prompt="You are a data analysis expert.",
        settings=settings,
    )

    # Get statistics
    stats = get_task_statistics(result.get("tasks", []))
    print("\n📊 Statistics:")
    print(f"   Success Rate: {stats['success_rate']}%")
    print(f"   Total Tasks: {stats['total_tasks']}")
    print(f"   Completed: {stats['completed']}")
    print(f"   Failed: {stats['failed']}")


async def example_with_monitoring():
    """Example with detailed monitoring."""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: With Monitoring")
    print("=" * 60 + "\n")

    result = await run_agent(
        user_request="Create a web scraper that extracts product information from an e-commerce website",
        system_prompt="You are a web scraping expert.",
    )

    # Format and print summary
    summary = format_execution_summary(result)
    print(summary)

    # Check for errors
    if result.get("error_message"):
        print(f"\n❌ Error occurred: {result['error_message']}")
    else:
        print("\n✅ Execution completed successfully!")

    # Save state
    filepath = save_state_to_file(result)
    print(f"\n💾 Full state saved to: {filepath}")


async def example_error_handling():
    """Example with error handling."""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Error Handling")
    print("=" * 60 + "\n")

    try:
        result = await run_agent(
            user_request="Perform an impossible task that will likely fail",
            system_prompt="You are a helpful assistant.",
        )

        if result.get("error_message"):
            logger.error(f"Task failed: {result['error_message']}")

            # Analyze failed tasks
            failed_tasks = [
                t for t in result.get("tasks", []) if t.status.value == "failed"
            ]
            for task in failed_tasks:
                logger.error(f"Failed Task: {task.title}")
                logger.error(f"Error: {task.error}")
        else:
            logger.info("Task completed successfully!")

    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)


async def main():
    """Run all examples."""

    # Ensure .env file exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your API keys.")
        print("You can copy .env.example to .env and edit it.")
        return

    # Check if API key is set
    settings = get_settings()
    if (
        not settings.openai_api_key
        or settings.openai_api_key == "your-openai-api-key-here"
    ):
        print("⚠️  Warning: OPENAI_API_KEY not set in .env file!")
        print("Please set your API key in the .env file.")
        return

    print("\n" + "=" * 60)
    print("🤖 LangGraph + PydanticAI Agent System Examples")
    print("=" * 60)

    # Run examples (uncomment the ones you want to run)

    # await example_basic()
    # await example_custom_models()
    # await example_with_monitoring()
    # await example_error_handling()

    # Run a simple test
    print("\n" + "=" * 60)
    print("Running Simple Test Example")
    print("=" * 60 + "\n")

    result = await run_agent(
        user_request="Create a simple 'Hello World' program in Python with proper documentation",
        system_prompt="You are a helpful programming assistant.",
    )

    print("\n" + "=" * 60)
    print("✅ Example completed!")
    print("=" * 60)

    # Print final summary
    if result.get("final_summary"):
        print(result["final_summary"])


if __name__ == "__main__":
    asyncio.run(main())
