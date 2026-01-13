"""Mocked tools for DevOps Dependency Hell test."""
from typing import Dict, List, Union

# Mock state
installed_packages = {"requests": "1.0", "authlib": "1.0"}


def pip_install(package: str) -> str:
    """Installs a python package. Format: package==version or just package."""
    global installed_packages
    if "==" in package:
        name, version = package.split("==")
        installed_packages[name.strip()] = version.strip()
    else:
        # Default to latest if no version specified
        if package.strip() == "requests":
            installed_packages["requests"] = "2.0"
        elif package.strip() == "authlib":
            installed_packages["authlib"] = "2.0"
    return f"Successfully installed {package}"


def pip_list() -> str:
    """Lists installed packages."""
    return ", ".join([f"{k}=={v}" for k, v in installed_packages.items()])


def run_tests() -> str:
    """Runs the test suite."""
    req_ver = installed_packages.get("requests", "0")
    auth_ver = installed_packages.get("authlib", "0")

    if req_ver == "2.0" and auth_ver == "1.0":
        return "FAIL: authlib 1.0 is incompatible with requests 2.0. Requires requests<2.0 or upgrade authlib."

    if req_ver == "2.0" and auth_ver == "2.0":
        return "PASS: All tests passed."

    return "PASS: Tests passed (but maybe not updated?)"


def read_error_log() -> str:
    """Reads the last error log."""
    return "Log: Dependency conflict detected during test run."


def revert_changes() -> str:
    """Reverts to the initial state."""
    global installed_packages
    installed_packages = {"requests": "1.0", "authlib": "1.0"}
    return "Reverted to initial state."


def get_tools() -> List[Dict[str, Union[str, callable]]]:
    """Get the tool definitions for the agent."""
    return [
        {
            "name": "pip_install",
            "description": "Installs a package.",
            "function": pip_install,
        },
        {
            "name": "pip_list",
            "description": "Lists installed packages.",
            "function": pip_list,
        },
        {
            "name": "run_tests",
            "description": "Runs tests to verify compatibility.",
            "function": run_tests,
        },
        {
            "name": "read_error_log",
            "description": "Reads error logs.",
            "function": read_error_log,
        },
        {
            "name": "revert_changes",
            "description": "Reverts changes if stuck.",
            "function": revert_changes,
        },
    ]
