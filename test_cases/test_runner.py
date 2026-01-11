import json
import importlib.util
import inspect
from pathlib import Path
import traceback
from typing import Any, List
from datetime import datetime


class TestRunner:
    """Test runner that dynamically loads and runs all test cases."""

    def __init__(self, agent_func: callable):
        self.agent_func = agent_func
        self.test_dir = Path(__file__).parent
        self._load_test_cases()

    def _load_test_cases(self):
        """Dynamically load all test case directories."""
        self.test_cases = [
            d.name
            for d in self.test_dir.iterdir()
            if d.is_dir() and (d / "config.json").exists()
        ]

    def _load_test_data(self, test_name: str):
        """Load all test data for a test case."""
        import sys

        if str(self.test_dir) not in sys.path:
            sys.path.append(str(self.test_dir))

        test_path = self.test_dir / test_name

        with open(test_path / "config.json") as f:
            config = json.load(f)
        with open(test_path / "expected_output.json") as f:
            expected = json.load(f)

        # Load output schema - get the main output class
        spec = importlib.util.spec_from_file_location(
            "schema", test_path / "output_schema.py"
        )
        schema_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(schema_mod)

        # Find the main output class (ends with 'Output')
        output_type = None
        for name, obj in schema_mod.__dict__.items():
            if isinstance(obj, type) and name.endswith("Output"):
                output_type = obj
                break

        if output_type is None:
            # Fallback to last class if no 'Output' class found
            output_type = next(
                v for v in schema_mod.__dict__.values() if isinstance(v, type)
            )

        # Load tools
        spec = importlib.util.spec_from_file_location(
            "tools", test_path / "mocked_tools.py"
        )
        tools_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(tools_mod)
        tools = tools_mod.get_tools()

        # Load evaluator
        spec = importlib.util.spec_from_file_location(
            "eval", test_path / "evaluator.py"
        )
        eval_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(eval_mod)

        return config, expected, output_type, tools, eval_mod.evaluate

    async def test_batch_research(self):
        """Test batch research workflow."""
        return await self._run_test("batch_research")

    async def test_context_compression(self):
        """Test context compression workflow."""
        return await self._run_test("context_compression")

    async def test_extraction_audit(self):
        """Test extraction audit workflow."""
        return await self._run_test("extraction_audit")

    async def test_parallel_doc_triage(self):
        """Test parallel document triage workflow."""
        return await self._run_test("parallel_doc_triage")

    async def test_planner_workers_join(self):
        """Test planner workers join workflow."""
        return await self._run_test("planner_workers_join")

    async def test_rca_fix_test(self):
        """Test RCA fix workflow."""
        return await self._run_test("rca_fix_test")

    async def test_safe_ops_approval(self):
        """Test safe ops approval workflow."""
        return await self._run_test("safe_ops_approval")

    async def test_tool_conflict_resolution(self):
        """Test tool conflict resolution workflow."""
        return await self._run_test("tool_conflict_resolution")

    async def _run_test(self, test_name: str) -> bool:
        """Run a single test case."""
        config, expected, output_type, tools, evaluate = self._load_test_data(test_name)

        result = await self.agent_func(
            system_prompt=config["system_prompt"],
            user_prompt=config["user_prompt"],
            output_type=output_type,
            tools=tools,
        )

        if result:
            # Save agent output to outputs folder
            self._save_output(test_name, result)

            if inspect.iscoroutinefunction(evaluate):
                return await evaluate(result.dict(), expected)
            else:
                return evaluate(result.dict(), expected)
        else:
            return False

    def _save_output(self, test_name: str, result: Any):
        """Save agent output to outputs folder."""
        outputs_dir = Path(__file__).parent.parent / "outputs"
        outputs_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{test_name}_output_{timestamp}.json"

        output_data = {
            "test_name": test_name,
            "timestamp": datetime.now().isoformat(),
            "agent_output": result.dict() if hasattr(result, "dict") else result,
        }

        with open(outputs_dir / filename, "w") as f:
            json.dump(output_data, f, indent=2)

    async def run_all(self) -> List[tuple[str, bool]]:
        """Run all test cases."""
        results = []
        for test_name in sorted(self.test_cases):
            print(f"Running {test_name}...")
            try:
                method_name = f"test_{test_name}"
                test_method = getattr(self, method_name)
                passed = await test_method()
                results.append((test_name, passed))
                print(f"  {'PASS' if passed else 'FAIL'}")
            except Exception as e:
                results.append((test_name, False))
                print(f"  FAIL: {e}")
                print(traceback.print_exc())
        return results


async def run_tests(agent_func: callable) -> List[tuple[str, bool]]:
    """Run all tests with the given agent function."""
    runner = TestRunner(agent_func)
    return await runner.run_all()


async def run_test(test_name: str, agent_func: callable) -> bool:
    """Run a specific test case.

    Args:
        test_name: Name of the test case (e.g., 'batch_research')
        agent_func: Async agent function

    Returns:
        True if test passed, False otherwise
    """
    runner = TestRunner(agent_func)
    return await runner._run_test(test_name)
