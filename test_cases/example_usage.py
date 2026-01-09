"""
Example usage of the multi-agent test framework.

This script demonstrates how to run the test cases with your agent implementation.
"""
import sys
from pathlib import Path

# Add test_cases directory to path
sys.path.insert(0, str(Path(__file__).parent))

from test_runner import run_test_case, run_all_tests, save_results


def example_agent_runner(system_prompt: str, user_prompt: str, tools: list, input_data: dict):
    """
    Example agent runner function.
    
    Replace this with your actual multi-agent implementation.
    
    Args:
        system_prompt: System prompt for the agent
        user_prompt: User prompt/task
        tools: List of available tools
        input_data: Input data for the task
        
    Returns:
        Agent output (should match expected output structure)
    """
    # This is a placeholder - replace with your actual agent implementation
    # For example, using your LangGraph + PydanticAI agent:
    
    # from langgraph_pydantic_agent import MultiAgentWorkflow
    # 
    # workflow = MultiAgentWorkflow(
    #     system_prompt=system_prompt,
    #     tools=tools
    # )
    # 
    # result = workflow.run(
    #     user_message=user_prompt,
    #     input_data=input_data
    # )
    # 
    # return result
    
    # Placeholder return
    return {
        "status": "not_implemented",
        "message": "Replace example_agent_runner with your actual agent implementation"
    }


def run_single_test_example():
    """Example: Run a single test case."""
    print("=" * 60)
    print("Running Single Test: Parallel Document Triage")
    print("=" * 60)
    
    result = run_test_case("01_parallel_doc_triage", example_agent_runner)
    
    print(f"\nTest: {result.test_name}")
    print(f"Passed: {result.passed}")
    print(f"Overall Score: {result.overall_score:.1f}/100")
    print(f"\nDetailed Scores:")
    print(f"  Correctness: {result.correctness_score:.1f}/100")
    print(f"  Consistency: {result.consistency_score:.1f}/100")
    print(f"  Conflict Handling: {result.conflict_handling_score:.1f}/100")
    print(f"  Traceability: {result.traceability_score:.1f}/100")
    print(f"\nExecution Time: {result.execution_time:.2f}s")
    
    if result.errors:
        print(f"\nErrors:")
        for error in result.errors:
            print(f"  - {error}")


def run_all_tests_example():
    """Example: Run all test cases."""
    print("=" * 60)
    print("Running All Test Cases")
    print("=" * 60)
    
    results = run_all_tests(example_agent_runner)
    
    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    avg_score = sum(r.overall_score for r in results) / len(results) if results else 0
    
    print(f"\nTotal Tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Average Score: {avg_score:.1f}/100")
    
    print("\nIndividual Results:")
    for result in results:
        status = "✓" if result.passed else "✗"
        print(f"  {status} {result.test_name}: {result.overall_score:.1f}/100")
    
    # Save results
    save_results(results)


def run_specific_tests_example():
    """Example: Run specific test cases."""
    test_cases = [
        "01_parallel_doc_triage",
        "02_extraction_audit",
        "03_tool_conflict_resolution"
    ]
    
    print("=" * 60)
    print("Running Specific Test Cases")
    print("=" * 60)
    
    results = []
    for test_name in test_cases:
        print(f"\nRunning: {test_name}")
        result = run_test_case(test_name, example_agent_runner)
        results.append(result)
        
        status = "✓ PASSED" if result.passed else "✗ FAILED"
        print(f"{status} - Score: {result.overall_score:.1f}/100")
    
    # Save results
    save_results(results, Path(__file__).parent / "specific_tests_results.json")


if __name__ == "__main__":
    print("""
Multi-Agent Test Framework
===========================

This framework provides 8 test cases designed to evaluate multi-agent workflows.

Before running tests:
1. Implement your agent runner function (replace example_agent_runner)
2. Ensure your agent can handle the expected input/output formats
3. Review individual test case READMEs for specific requirements

Available examples:
1. run_single_test_example() - Run one test case
2. run_all_tests_example() - Run all 8 test cases
3. run_specific_tests_example() - Run selected test cases

Uncomment the example you want to run below:
""")
    
    # Uncomment one of these to run:
    # run_single_test_example()
    # run_all_tests_example()
    # run_specific_tests_example()
    
    print("\nTo run tests, uncomment one of the example functions in the main block.")
