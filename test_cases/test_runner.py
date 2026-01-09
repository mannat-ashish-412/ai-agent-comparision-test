"""
Test runner for multi-agent workflow evaluation.
"""
import json
import time
from pathlib import Path
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime


@dataclass
class TestResult:
    """Result of a single test case execution."""
    test_name: str
    passed: bool
    correctness_score: float
    consistency_score: float
    conflict_handling_score: float
    traceability_score: float
    execution_time: float
    errors: List[str]
    output: Any
    
    @property
    def overall_score(self) -> float:
        """Calculate overall score as average of all metrics."""
        return (
            self.correctness_score + 
            self.consistency_score + 
            self.conflict_handling_score + 
            self.traceability_score
        ) / 4
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary."""
        return {
            "test_name": self.test_name,
            "passed": self.passed,
            "scores": {
                "correctness": self.correctness_score,
                "consistency": self.consistency_score,
                "conflict_handling": self.conflict_handling_score,
                "traceability": self.traceability_score,
                "overall": self.overall_score
            },
            "execution_time": self.execution_time,
            "errors": self.errors,
            "output": self.output
        }


class TestCaseRunner:
    """Runner for individual test cases."""
    
    def __init__(self, test_cases_dir: Path = None):
        """Initialize test runner.
        
        Args:
            test_cases_dir: Path to test cases directory
        """
        if test_cases_dir is None:
            test_cases_dir = Path(__file__).parent
        self.test_cases_dir = test_cases_dir
    
    def load_test_config(self, test_name: str) -> Dict[str, Any]:
        """Load test configuration.
        
        Args:
            test_name: Name of the test case
            
        Returns:
            Test configuration dictionary
        """
        config_path = self.test_cases_dir / test_name / "config.json"
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_input_data(self, test_name: str) -> Any:
        """Load test input data.
        
        Args:
            test_name: Name of the test case
            
        Returns:
            Input data
        """
        input_path = self.test_cases_dir / test_name / "input_data.json"
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_expected_output(self, test_name: str) -> Dict[str, Any]:
        """Load expected output structure.
        
        Args:
            test_name: Name of the test case
            
        Returns:
            Expected output dictionary
        """
        output_path = self.test_cases_dir / test_name / "expected_output.json"
        with open(output_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def load_mocked_tools(self, test_name: str):
        """Load mocked tools for the test.
        
        Args:
            test_name: Name of the test case
            
        Returns:
            Module containing mocked tools
        """
        import importlib.util
        
        tools_path = self.test_cases_dir / test_name / "mocked_tools.py"
        spec = importlib.util.spec_from_file_location(
            f"{test_name}_tools", 
            tools_path
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    
    def evaluate_output(
        self, 
        test_name: str, 
        actual_output: Any, 
        expected_output: Dict[str, Any]
    ) -> Dict[str, float]:
        """Evaluate test output against expected criteria.
        
        Args:
            test_name: Name of the test case
            actual_output: Actual output from the agent
            expected_output: Expected output structure and criteria
            
        Returns:
            Dictionary of scores
        """
        # This is a placeholder - implement specific evaluation logic
        # based on test case requirements
        scores = {
            "correctness": 0.0,
            "consistency": 0.0,
            "conflict_handling": 0.0,
            "traceability": 0.0
        }
        
        # Load test-specific evaluator if available
        evaluator_path = self.test_cases_dir / test_name / "evaluator.py"
        if evaluator_path.exists():
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                f"{test_name}_evaluator", 
                evaluator_path
            )
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'evaluate'):
                scores = module.evaluate(actual_output, expected_output)
        
        return scores
    
    def run_test(
        self, 
        test_name: str, 
        agent_runner_func: callable
    ) -> TestResult:
        """Run a single test case.
        
        Args:
            test_name: Name of the test case
            agent_runner_func: Function that runs the agent workflow.
                Should accept (system_prompt, user_prompt, tools, input_data)
                and return the agent's output.
                
        Returns:
            TestResult object
        """
        errors = []
        output = None
        
        try:
            # Load test resources
            config = self.load_test_config(test_name)
            input_data = self.load_input_data(test_name)
            expected_output = self.load_expected_output(test_name)
            mocked_tools = self.load_mocked_tools(test_name)
            
            # Extract configuration
            system_prompt = config.get("system_prompt", "")
            user_prompt = config.get("user_prompt", "")
            tools = getattr(mocked_tools, 'get_tools', lambda: [])()
            
            # Run the agent
            start_time = time.time()
            output = agent_runner_func(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                tools=tools,
                input_data=input_data
            )
            execution_time = time.time() - start_time
            
            # Evaluate output
            scores = self.evaluate_output(test_name, output, expected_output)
            
            # Check if test passed (all scores >= 70)
            passed = all(score >= 70 for score in scores.values())
            
            return TestResult(
                test_name=test_name,
                passed=passed,
                correctness_score=scores["correctness"],
                consistency_score=scores["consistency"],
                conflict_handling_score=scores["conflict_handling"],
                traceability_score=scores["traceability"],
                execution_time=execution_time,
                errors=errors,
                output=output
            )
            
        except Exception as e:
            errors.append(str(e))
            return TestResult(
                test_name=test_name,
                passed=False,
                correctness_score=0.0,
                consistency_score=0.0,
                conflict_handling_score=0.0,
                traceability_score=0.0,
                execution_time=0.0,
                errors=errors,
                output=output
            )


def run_test_case(test_name: str, agent_runner_func: callable) -> TestResult:
    """Run a single test case.
    
    Args:
        test_name: Name of the test case
        agent_runner_func: Function to run the agent workflow
        
    Returns:
        TestResult object
    """
    runner = TestCaseRunner()
    return runner.run_test(test_name, agent_runner_func)


def run_all_tests(agent_runner_func: callable) -> List[TestResult]:
    """Run all test cases.
    
    Args:
        agent_runner_func: Function to run the agent workflow
        
    Returns:
        List of TestResult objects
    """
    runner = TestCaseRunner()
    test_cases_dir = Path(__file__).parent
    
    # Find all test case directories
    test_cases = [
        d.name for d in test_cases_dir.iterdir() 
        if d.is_dir() and (d / "config.json").exists()
    ]
    
    results = []
    for test_name in sorted(test_cases):
        print(f"\nRunning test: {test_name}")
        result = runner.run_test(test_name, agent_runner_func)
        results.append(result)
        
        # Print summary
        status = "✓ PASSED" if result.passed else "✗ FAILED"
        print(f"{status} - Overall Score: {result.overall_score:.1f}/100")
        if result.errors:
            print(f"  Errors: {', '.join(result.errors)}")
    
    return results


def save_results(results: List[TestResult], output_path: Path = None):
    """Save test results to JSON file.
    
    Args:
        results: List of TestResult objects
        output_path: Path to save results (default: test_results_<timestamp>.json)
    """
    if output_path is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = Path(__file__).parent / f"test_results_{timestamp}.json"
    
    results_dict = {
        "timestamp": datetime.now().isoformat(),
        "total_tests": len(results),
        "passed": sum(1 for r in results if r.passed),
        "failed": sum(1 for r in results if not r.passed),
        "average_score": sum(r.overall_score for r in results) / len(results) if results else 0,
        "results": [r.to_dict() for r in results]
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results_dict, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")


if __name__ == "__main__":
    print("Test runner loaded. Use run_test_case() or run_all_tests() to execute tests.")
