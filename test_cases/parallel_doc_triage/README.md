# Test Case 1: Parallel Document Triage

## Overview
This test evaluates the system's ability to process multiple items in parallel, classify them, identify duplicates, and maintain consistency across the workflow.

## Scenario
Process 10 bug reports and feature requests that include:
- 5 bugs (with 2 pairs of duplicates)
- 4 feature requests (with 2 duplicates)
- 1 question

## Multi-Agent Requirements
This test requires multiple specialized agents:

1. **Classifier Agent(s)**: Categorize each item as bug/feature/question
2. **Deduplication Agent**: Identify and merge duplicate items
3. **Severity Assessor**: Assign priority levels based on impact
4. **QA Reviewer**: Validate consistency and completeness

## Why Single Agent Fails
A single agent typically:
- Processes items sequentially, missing patterns across items
- Inconsistently applies classification rules
- Fails to maintain structured deduplication tracking
- Cannot provide clear traceability of decisions

## Expected Behavior
The multi-agent system should:
- Process items in parallel for efficiency
- Identify 4 duplicate pairs correctly
- Produce 6 unique items after deduplication
- Assign appropriate severity (1 critical, 1 high, 2 medium, 2 low)
- Provide clear agent trace showing which agent made each decision

## Pass Criteria
- **Correctness ≥ 70**: Correct classifications, duplicates identified, appropriate severity
- **Consistency ≥ 70**: No contradictions in output
- **Conflict Handling ≥ 70**: Duplicates properly merged with reasoning
- **Traceability ≥ 70**: Clear agent attribution for all decisions

## Time Limit
5 minutes

## Files
- `config.json` - Test configuration with prompts
- `input_data.json` - 10 issue reports
- `expected_output.json` - Expected structure and validation rules
- `mocked_tools.py` - Classification, similarity, and severity tools
- `evaluator.py` - Custom scoring logic
