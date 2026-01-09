"""
Validation script to check test case structure and integrity.
"""
import json
from pathlib import Path
from typing import List, Dict, Tuple


def validate_test_case(test_dir: Path) -> Tuple[bool, List[str]]:
    """
    Validate a single test case directory.
    
    Args:
        test_dir: Path to test case directory
        
    Returns:
        Tuple of (is_valid, list of errors)
    """
    errors = []
    required_files = [
        "config.json",
        "input_data.json",
        "expected_output.json",
        "mocked_tools.py",
        "evaluator.py",
        "README.md"
    ]
    
    # Check all required files exist
    for filename in required_files:
        filepath = test_dir / filename
        if not filepath.exists():
            errors.append(f"Missing required file: {filename}")
    
    # Validate config.json
    config_path = test_dir / "config.json"
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            required_keys = ["name", "system_prompt", "user_prompt", "required_agents"]
            for key in required_keys:
                if key not in config:
                    errors.append(f"config.json missing required key: {key}")
        except json.JSONDecodeError as e:
            errors.append(f"config.json is not valid JSON: {e}")
        except Exception as e:
            errors.append(f"Error reading config.json: {e}")
    
    # Validate input_data.json
    input_path = test_dir / "input_data.json"
    if input_path.exists():
        try:
            with open(input_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            errors.append(f"input_data.json is not valid JSON: {e}")
    
    # Validate expected_output.json
    expected_path = test_dir / "expected_output.json"
    if expected_path.exists():
        try:
            with open(expected_path, 'r', encoding='utf-8') as f:
                expected = json.load(f)
            
            if "structure" not in expected:
                errors.append("expected_output.json missing 'structure' key")
        except json.JSONDecodeError as e:
            errors.append(f"expected_output.json is not valid JSON: {e}")
    
    # Validate mocked_tools.py
    tools_path = test_dir / "mocked_tools.py"
    if tools_path.exists():
        try:
            with open(tools_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "def get_tools()" not in content:
                errors.append("mocked_tools.py missing get_tools() function")
        except Exception as e:
            errors.append(f"Error reading mocked_tools.py: {e}")
    
    # Validate evaluator.py
    evaluator_path = test_dir / "evaluator.py"
    if evaluator_path.exists():
        try:
            with open(evaluator_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if "def evaluate(" not in content:
                errors.append("evaluator.py missing evaluate() function")
        except Exception as e:
            errors.append(f"Error reading evaluator.py: {e}")
    
    is_valid = len(errors) == 0
    return is_valid, errors


def validate_all_test_cases() -> Dict[str, Tuple[bool, List[str]]]:
    """
    Validate all test cases.
    
    Returns:
        Dictionary mapping test name to (is_valid, errors)
    """
    test_cases_dir = Path(__file__).parent
    results = {}
    
    # Find all test case directories
    for item in test_cases_dir.iterdir():
        if item.is_dir() and item.name.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")):
            is_valid, errors = validate_test_case(item)
            results[item.name] = (is_valid, errors)
    
    return results


def print_validation_report():
    """Print validation report for all test cases."""
    print("=" * 70)
    print("Test Case Validation Report")
    print("=" * 70)
    
    results = validate_all_test_cases()
    
    if not results:
        print("\n❌ No test cases found!")
        return
    
    total = len(results)
    valid = sum(1 for is_valid, _ in results.values() if is_valid)
    invalid = total - valid
    
    print(f"\nTotal Test Cases: {total}")
    print(f"Valid: {valid}")
    print(f"Invalid: {invalid}")
    
    print("\n" + "-" * 70)
    print("Individual Test Case Results")
    print("-" * 70)
    
    for test_name in sorted(results.keys()):
        is_valid, errors = results[test_name]
        
        if is_valid:
            print(f"\n✅ {test_name}")
            print("   All required files present and valid")
        else:
            print(f"\n❌ {test_name}")
            for error in errors:
                print(f"   - {error}")
    
    print("\n" + "=" * 70)
    
    if invalid == 0:
        print("✅ All test cases are valid!")
    else:
        print(f"⚠️  {invalid} test case(s) need attention")
    
    print("=" * 70)


def check_test_runner():
    """Check if test_runner.py is present and valid."""
    test_runner_path = Path(__file__).parent / "test_runner.py"
    
    if not test_runner_path.exists():
        print("❌ test_runner.py not found!")
        return False
    
    try:
        with open(test_runner_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_functions = [
            "class TestCaseRunner",
            "def run_test_case(",
            "def run_all_tests(",
            "def save_results("
        ]
        
        missing = []
        for func in required_functions:
            if func not in content:
                missing.append(func)
        
        if missing:
            print(f"❌ test_runner.py missing: {', '.join(missing)}")
            return False
        
        print("✅ test_runner.py is valid")
        return True
        
    except Exception as e:
        print(f"❌ Error reading test_runner.py: {e}")
        return False


if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("Multi-Agent Test Suite Validation")
    print("=" * 70 + "\n")
    
    # Check test runner
    print("Checking test_runner.py...")
    check_test_runner()
    
    print("\n")
    
    # Validate all test cases
    print_validation_report()
    
    print("\n✨ Validation complete!\n")
