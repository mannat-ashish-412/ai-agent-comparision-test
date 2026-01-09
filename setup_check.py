"""
Setup script for the LangGraph + PydanticAI Agent System
Run this script to verify your setup and configuration.
"""

import sys
from pathlib import Path


def print_header(text):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60 + "\n")


def print_success(text):
    """Print success message."""
    print(f"✅ {text}")


def print_error(text):
    """Print error message."""
    print(f"❌ {text}")


def print_warning(text):
    """Print warning message."""
    print(f"⚠️  {text}")


def print_info(text):
    """Print info message."""
    print(f"ℹ️  {text}")


def check_python_version():
    """Check Python version."""
    print_header("Checking Python Version")

    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major >= 3 and version.minor >= 9:
        print_success("Python version is compatible (3.9+)")
        return True
    else:
        print_error("Python 3.9 or higher is required")
        return False


def check_dependencies():
    """Check if dependencies are installed."""
    print_header("Checking Dependencies")

    required_packages = [
        "langgraph",
        "pydantic_ai",
        "pydantic",
        "pydantic_settings",
        "openai",
        "aiosqlite",
    ]

    missing = []

    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} is installed")
        except ImportError:
            print_error(f"{package} is NOT installed")
            missing.append(package)

    if missing:
        print_warning("\nSome dependencies are missing!")
        print_info("Run: pip install -r requirements_langgraph.txt")
        return False

    return True


def check_env_file():
    """Check if .env file exists and is configured."""
    print_header("Checking Environment Configuration")

    env_file = Path(".env")
    env_example = Path(".env.example")

    if not env_file.exists():
        print_error(".env file not found")
        if env_example.exists():
            print_info("Run: copy .env.example .env")
            print_info("Then edit .env with your API keys")
        return False

    print_success(".env file exists")

    # Check if API key is set
    with open(env_file, "r") as f:
        content = f.read()

    if "your-openai-api-key-here" in content or "OPENAI_API_KEY=" not in content:
        print_warning("OPENAI_API_KEY may not be configured")
        print_info("Edit .env and set your API key")
        return False

    print_success("OPENAI_API_KEY appears to be set")
    return True


def check_directories():
    """Check if required directories exist."""
    print_header("Checking Directories")

    dirs = ["logs", "checkpoints", "outputs"]

    for dir_name in dirs:
        dir_path = Path(dir_name)
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
            print_info(f"Created directory: {dir_name}/")
        else:
            print_success(f"Directory exists: {dir_name}/")

    return True


def check_files():
    """Check if all required files exist."""
    print_header("Checking Required Files")

    required_files = [
        "langgraph_pydantic_agent.py",
        "config.py",
        "logger.py",
        "exceptions.py",
        "utils.py",
        "requirements_langgraph.txt",
        ".env.example",
    ]

    all_exist = True

    for filename in required_files:
        file_path = Path(filename)
        if file_path.exists():
            print_success(f"{filename}")
        else:
            print_error(f"{filename} is MISSING")
            all_exist = False

    return all_exist


def test_import():
    """Test importing the main module."""
    print_header("Testing Module Import")

    try:
        from config import get_settings

        print_success("config module imported successfully")

        settings = get_settings()
        print_info(f"Default model: {settings.default_model}")
        print_info(f"Max attempts: {settings.task_config.max_attempts}")
        print_info(f"Max iterations: {settings.task_config.max_iterations}")

        return True
    except Exception as e:
        print_error(f"Failed to import config: {e}")
        return False


def print_next_steps():
    """Print next steps for the user."""
    print_header("Next Steps")

    print("1. If dependencies are missing:")
    print("   pip install -r requirements_langgraph.txt\n")

    print("2. If .env is not configured:")
    print("   copy .env.example .env")
    print("   notepad .env  # Add your API key\n")

    print("3. Run the example:")
    print("   python example.py\n")

    print("4. Read the documentation:")
    print("   - QUICKSTART.md for quick start")
    print("   - LANGGRAPH_AGENT_README.md for full docs")
    print("   - PROJECT_SUMMARY.md for overview\n")


def main():
    """Run all checks."""
    print("\n" + "=" * 60)
    print("  LangGraph + PydanticAI Agent System Setup")
    print("=" * 60)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Environment File", check_env_file),
        ("Directories", check_directories),
        ("Required Files", check_files),
        ("Module Import", test_import),
    ]

    results = []

    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print_error(f"Error during {name} check: {e}")
            results.append((name, False))

    # Summary
    print_header("Setup Summary")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")

    print(f"\nPassed: {passed}/{total}")

    if passed == total:
        print_success("\n🎉 All checks passed! You're ready to go!")
        print_info("\nRun: python example.py")
    else:
        print_warning("\n⚠️  Some checks failed. Please fix the issues above.")
        print_next_steps()

    print("\n" + "=" * 60 + "\n")


if __name__ == "__main__":
    main()
