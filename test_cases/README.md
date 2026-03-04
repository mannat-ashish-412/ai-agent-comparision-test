# Multi-Agent Workflow Test Cases

This folder contains 8 real-world test cases designed to evaluate multi-agent workflows. Each test case is structured to favor multi-agent architectures over single-agent approaches.

## Test Case Structure

Each test case folder contains:
- `config.json` - Test configuration with system/user prompts and expected outputs
- `mocked_tools.py` - Mocked tool implementations for the test
- `input_data.json` - Input data for the test case
- `expected_output.json` - Expected output structure and validation criteria
- `README.md` - Detailed description and evaluation criteria

## Test Cases Overview

1. **parallel_doc_triage** - Parallel processing of 10 bug reports with classification, deduplication, and severity assessment
2. **extraction_audit** - Two-step extraction with consistency auditing and contradiction detection
3. **tool_conflict_resolution** - Handling conflicting tool outputs with adjudication
4. **planner_workers_join** - Decomposition, parallel execution, and merging of migration plan
5. **rca_fix_test** - Root cause analysis, fix proposal, and regression test generation
6. **safe_ops_approval** - Human-in-the-loop approval gate for unsafe operations
7. **context_compression** - Long conversation history compression and task solving
8. **batch_research** - Parallel knowledge base retrieval with citation synthesis

## Running Tests

```python
from test_runner import run_test_case

# Run a single test
result = run_test_case("parallel_doc_triage")

# Run all tests
from test_runner import run_all_tests
results = run_all_tests()
```

## Evaluation Criteria

Each test is scored on:
- **Correctness** (0-100): Does the output match expected structure and content?
- **Consistency** (0-100): Are there internal contradictions?
- **Conflict Handling** (0-100): Are conflicts explicitly detected and resolved?
- **Traceability** (0-100): Can we trace which agent produced what?

## Time Limits

Each test should complete within 5 minutes using mocked tools.
