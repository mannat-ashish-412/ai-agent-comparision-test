# Multi-Agent Test Cases - Quick Reference

## Test Case Summary

| # | Name | Focus | Key Challenge | Time |
|---|------|-------|---------------|------|
| 1 | Parallel Doc Triage | Parallel processing + deduplication | 10 items, 4 duplicate pairs | 5min |
| 2 | Extraction + Audit | Role separation (extract vs audit) | 9 contradictions in requirements | 5min |
| 3 | Tool Conflict Resolution | Conflicting data sources | 2 tools return different prices | 5min |
| 4 | Planner-Workers-Join | Decomposition + merge | 3 subtasks, consistency check | 5min |
| 5 | RCA + Fix + Test | Diagnosis separation | Root cause → patch → tests | 5min |
| 6 | Safe Ops Approval | Human-in-the-loop gate | Must NOT auto-execute delete | 5min |
| 7 | Context Compression | Long history management | 30 messages, 1 key update | 5min |
| 8 | Batch Research | Parallel retrieval + citations | 5 questions, must cite sources | 5min |

## Scoring Criteria

Each test is scored on 4 metrics (0-100 each):

1. **Correctness**: Does output match expected structure and content?
2. **Consistency**: Are there internal contradictions?
3. **Conflict Handling**: Are conflicts explicitly detected and resolved?
4. **Traceability**: Can we trace which agent did what?

**Pass Threshold**: All 4 scores ≥ 70

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements_langgraph.txt
```

### 2. Implement Agent Runner
```python
def my_agent_runner(system_prompt, user_prompt, tools, input_data):
    # Your multi-agent implementation here
    # Return output matching expected structure
    return result
```

### 3. Run Tests
```python
from test_runner import run_test_case

result = run_test_case("01_parallel_doc_triage", my_agent_runner)
print(f"Score: {result.overall_score}/100")
```

## File Structure

Each test case folder contains:
```
XX_test_name/
├── config.json           # System/user prompts, requirements
├── input_data.json       # Test input data
├── expected_output.json  # Expected structure & validation rules
├── mocked_tools.py       # Tool implementations
├── evaluator.py          # Custom scoring logic
└── README.md            # Detailed description
```

## Expected Output Formats

### Test 1: Parallel Doc Triage
```json
{
  "processed_items": [...],
  "duplicates_merged": [...],
  "agent_trace": {...}
}
```

### Test 2: Extraction + Audit
```json
{
  "prd": {...},
  "contradictions": [...],
  "clarifying_questions": [...],
  "resolution_status": {...}
}
```

### Test 3: Tool Conflict Resolution
```json
{
  "detected_conflicts": [...],
  "resolution_policy": "freshness|authority|consensus",
  "final_price": 999,
  "audit_trail": {...}
}
```

### Test 4: Planner-Workers-Join
```json
{
  "subtasks": [...],
  "subtask_results": [...],
  "merged_plan": {...},
  "consistency_check": {...}
}
```

### Test 5: RCA + Fix + Test
```json
{
  "root_cause": "...",
  "proposed_patch": "...",
  "regression_tests": [...],
  "test_explanations": "..."
}
```

### Test 6: Safe Ops Approval
```json
{
  "unsafe_operations": [...],
  "safe_plan": "...",
  "approval_requested": true,
  "execution_status": "pending_approval"
}
```

### Test 7: Context Compression
```json
{
  "compressed_state": "...",
  "key_facts": [...],
  "final_answer": "...",
  "sources": [...]
}
```

### Test 8: Batch Research
```json
{
  "answers": [...],
  "citations": {...},
  "synthesis": "..."
}
```

## Common Pitfalls

### Single Agent Failures
- **Test 1**: Processes items sequentially, inconsistent classification
- **Test 2**: Overfits to one interpretation, ignores contradictions
- **Test 3**: Silently picks one value without acknowledging conflict
- **Test 4**: Produces internally inconsistent plans
- **Test 5**: Mixes diagnosis and solution, hallucinated fixes
- **Test 6**: Auto-executes unsafe operations
- **Test 7**: Gets brittle with long context, misses updates
- **Test 8**: Serializes calls, loses attribution

### Multi-Agent Success Patterns
- **Parallel Processing**: Workers handle items concurrently
- **Role Separation**: Distinct agents for extraction vs validation
- **Explicit Conflict Detection**: Dedicated conflict detector agent
- **Merge + Validate**: Joiner ensures consistency across workers
- **Staged Workflow**: Diagnosis → Fix → Test as separate stages
- **Approval Gates**: Safety checker before execution
- **Context Management**: Summarizer + Solver separation
- **Attribution Tracking**: Each agent logs its contributions

## Debugging Tips

1. **Check agent trace**: Ensure multiple agents are actually being used
2. **Verify tool calls**: Mocked tools should be called appropriately
3. **Review output structure**: Must match expected format exactly
4. **Test incrementally**: Start with one test case, then expand
5. **Read evaluator code**: Understand how scoring works

## Integration with Your System

### LangGraph Integration
```python
from langgraph_pydantic_agent import MultiAgentWorkflow

def langgraph_agent_runner(system_prompt, user_prompt, tools, input_data):
    workflow = MultiAgentWorkflow(
        system_prompt=system_prompt,
        tools=tools
    )
    result = workflow.run(
        user_message=user_prompt,
        input_data=input_data
    )
    return result
```

### PydanticAI Integration
```python
from pydantic_ai import Agent

def pydantic_agent_runner(system_prompt, user_prompt, tools, input_data):
    agent = Agent(
        model='openai:gpt-4',
        system_prompt=system_prompt,
        tools=tools
    )
    result = agent.run_sync(user_prompt, message_history=[])
    return result.data
```

## Results Analysis

After running tests, review:
- `test_results_YYYYMMDD_HHMMSS.json` - Detailed results
- Individual test scores and errors
- Overall pass/fail rate
- Areas for improvement

## Next Steps

1. Run all tests to establish baseline
2. Identify failing tests
3. Analyze why multi-agent approach is needed
4. Implement/refine agent architecture
5. Re-run tests to measure improvement
6. Iterate until all tests pass (≥70 on all metrics)
