# Multi-Agent Workflow Test Suite - Complete Overview

## 📋 What Has Been Created

A comprehensive test suite with **8 real-world test cases** designed to evaluate multi-agent workflows. Each test case strongly favors multi-agent architectures over single-agent approaches.

## 📁 Directory Structure

```
test_cases/
├── README.md                          # Main overview
├── QUICK_REFERENCE.md                 # Quick reference guide
├── test_runner.py                     # Test execution framework
├── example_usage.py                   # Usage examples
│
├── 01_parallel_doc_triage/           # Test Case 1
│   ├── config.json                    # System/user prompts
│   ├── input_data.json                # 10 bug reports with duplicates
│   ├── expected_output.json           # Validation criteria
│   ├── mocked_tools.py                # Classification & dedup tools
│   ├── evaluator.py                   # Custom scoring logic
│   └── README.md                      # Test description
│
├── 02_extraction_audit/              # Test Case 2
│   ├── config.json
│   ├── input_data.json                # Requirements with 9 contradictions
│   ├── expected_output.json
│   ├── mocked_tools.py                # Extraction & audit tools
│   ├── evaluator.py
│   └── README.md
│
├── 03_tool_conflict_resolution/      # Test Case 3
│   ├── config.json
│   ├── input_data.json                # Product query
│   ├── expected_output.json
│   ├── mocked_tools.py                # Tools returning conflicting prices
│   ├── evaluator.py
│   └── README.md
│
├── 04_planner_workers_join/          # Test Case 4
│   ├── config.json
│   ├── input_data.json                # MongoDB schema
│   ├── expected_output.json
│   ├── mocked_tools.py                # Schema analysis tools
│   ├── evaluator.py
│   └── README.md
│
├── 05_rca_fix_test/                  # Test Case 5
│   ├── config.json
│   ├── input_data.json                # Failing CI log
│   ├── expected_output.json
│   ├── mocked_tools.py                # Debug & patch tools
│   ├── evaluator.py
│   └── README.md
│
├── 06_safe_ops_approval/             # Test Case 6
│   ├── config.json
│   ├── input_data.json                # Unsafe delete request
│   ├── expected_output.json
│   ├── mocked_tools.py                # Safety classification tools
│   ├── evaluator.py
│   └── README.md
│
├── 07_context_compression/           # Test Case 7
│   ├── config.json
│   ├── input_data.json                # 30-message conversation
│   ├── expected_output.json
│   ├── mocked_tools.py                # Summarization tools
│   ├── evaluator.py
│   └── README.md
│
└── 08_batch_research/                # Test Case 8
    ├── config.json
    ├── input_data.json                # 5 questions + KB
    ├── expected_output.json
    ├── mocked_tools.py                # KB search tools
    ├── evaluator.py
    └── README.md
```

**Total Files**: 52 files across 8 test cases

## 🎯 Test Cases Overview

### 1. Parallel Document Triage
- **Input**: 10 bug reports/feature requests (4 duplicate pairs)
- **Challenge**: Classify, deduplicate, assign severity in parallel
- **Multi-Agent Pattern**: Classifier workers + Deduplicator + Severity assessor + QA reviewer
- **Why Single Agent Fails**: Sequential processing, inconsistent classification

### 2. Extraction + Consistency Audit
- **Input**: Requirements document with 9 contradictions
- **Challenge**: Extract structured PRD and identify all contradictions
- **Multi-Agent Pattern**: Extractor + Auditor + Clarification generator
- **Why Single Agent Fails**: Overfits to one interpretation, ignores conflicts

### 3. Tool Output Conflict Resolution
- **Input**: Product pricing query
- **Challenge**: Handle conflicting prices from 2 data sources (₹999 vs ₹1,099)
- **Multi-Agent Pattern**: Data collector + Conflict detector + Arbitrator + Auditor
- **Why Single Agent Fails**: Silently picks one value without reasoning

### 4. Planner-Workers-Join
- **Input**: MongoDB → DynamoDB migration schema
- **Challenge**: Decompose into 3 subtasks, execute, merge consistently
- **Multi-Agent Pattern**: Planner + 3 Workers + Joiner + Validator
- **Why Single Agent Fails**: Produces internally inconsistent plans

### 5. RCA + Fix + Regression Tests
- **Input**: Failing CI log (email validation bug)
- **Challenge**: Diagnose, propose patch, write regression tests
- **Multi-Agent Pattern**: Debugger + Fixer + Tester
- **Why Single Agent Fails**: Mixes diagnosis and solution, hallucinated fixes

### 6. Safe Operations Approval Gate
- **Input**: Request to delete production S3 bucket
- **Challenge**: Identify unsafe operation, request approval, don't auto-execute
- **Multi-Agent Pattern**: Analyzer + Safety planner + Approval gate
- **Why Single Agent Fails**: Complies too quickly without safety checks

### 7. Long Context Compression
- **Input**: 30-message conversation with key update (PostgreSQL → RDS)
- **Challenge**: Compress history and answer question from compressed state
- **Multi-Agent Pattern**: Summarizer + Solver
- **Why Single Agent Fails**: Gets brittle with long context, misses updates

### 8. Batch Knowledge Base Research
- **Input**: 5 questions about company policies
- **Challenge**: Retrieve answers in parallel with proper citations
- **Multi-Agent Pattern**: Worker agents + Synthesizer
- **Why Single Agent Fails**: Serializes calls, loses attribution

## 📊 Evaluation Framework

### Scoring Metrics (0-100 each)
1. **Correctness**: Output matches expected structure and content
2. **Consistency**: No internal contradictions
3. **Conflict Handling**: Conflicts explicitly detected and resolved
4. **Traceability**: Can trace which agent did what

### Pass Criteria
- All 4 metrics ≥ 70
- Overall score (average) ≥ 70

### Time Limits
- Each test: 5 minutes maximum
- All tests use mocked tools for speed

## 🚀 How to Use

### 1. Basic Usage
```python
from test_runner import run_test_case

def my_agent_runner(system_prompt, user_prompt, tools, input_data):
    # Your multi-agent implementation
    return result

# Run single test
result = run_test_case("01_parallel_doc_triage", my_agent_runner)
print(f"Score: {result.overall_score}/100")
```

### 2. Run All Tests
```python
from test_runner import run_all_tests, save_results

results = run_all_tests(my_agent_runner)
save_results(results)
```

### 3. View Results
```python
for result in results:
    print(f"{result.test_name}: {result.overall_score}/100")
    print(f"  Correctness: {result.correctness_score}")
    print(f"  Consistency: {result.consistency_score}")
    print(f"  Conflict Handling: {result.conflict_handling_score}")
    print(f"  Traceability: {result.traceability_score}")
```

## 🔧 Integration with Your System

### Required Interface
Your agent runner must accept:
- `system_prompt` (str): System instructions
- `user_prompt` (str): User task/question
- `tools` (list): Available tool functions
- `input_data` (dict): Test input data

And return:
- Output matching expected structure (see QUICK_REFERENCE.md)

### Example: LangGraph Integration
```python
from langgraph_pydantic_agent import MultiAgentWorkflow

def langgraph_runner(system_prompt, user_prompt, tools, input_data):
    workflow = MultiAgentWorkflow(
        system_prompt=system_prompt,
        tools=tools
    )
    return workflow.run(user_prompt, input_data)
```

## 📈 Expected Results

### Baseline (Single Agent)
- Expected pass rate: 0-25%
- Common failures:
  - Low traceability (no agent separation)
  - Poor conflict handling (silent failures)
  - Inconsistent outputs

### Target (Multi-Agent)
- Expected pass rate: 75-100%
- Success indicators:
  - Clear agent attribution
  - Explicit conflict detection
  - Consistent, traceable decisions

## 🎓 Learning Outcomes

By running these tests, you'll understand:
1. **When multi-agent is necessary** (vs single agent)
2. **Role separation benefits** (extraction vs audit, diagnosis vs fix)
3. **Parallel processing patterns** (workers + synthesizer)
4. **Conflict resolution strategies** (explicit detection + adjudication)
5. **Context management** (summarization + compression)
6. **Safety patterns** (approval gates, human-in-the-loop)

## 📝 Customization

### Adding New Test Cases
1. Create new directory: `09_your_test_name/`
2. Add required files:
   - `config.json` - Prompts and requirements
   - `input_data.json` - Test input
   - `expected_output.json` - Validation rules
   - `mocked_tools.py` - Tool implementations
   - `evaluator.py` - Scoring logic
   - `README.md` - Description

### Modifying Evaluators
Each `evaluator.py` contains custom scoring logic. Modify to:
- Adjust scoring weights
- Add new validation rules
- Change pass thresholds

## 🐛 Troubleshooting

### Common Issues
1. **Import errors**: Ensure test_cases directory is in Python path
2. **Tool not found**: Check mocked_tools.py exports get_tools()
3. **Low scores**: Review evaluator.py to understand scoring
4. **Timeout**: Reduce input size or optimize agent implementation

### Debug Mode
```python
result = run_test_case("01_parallel_doc_triage", my_agent_runner)
print(result.output)  # See actual agent output
print(result.errors)  # See any errors
```

## 📚 Additional Resources

- **README.md**: High-level overview
- **QUICK_REFERENCE.md**: Quick start guide with formats
- **example_usage.py**: Complete usage examples
- **Individual test READMEs**: Detailed test descriptions

## 🎯 Next Steps

1. ✅ Review QUICK_REFERENCE.md for formats
2. ✅ Implement your agent runner function
3. ✅ Run example_usage.py to test integration
4. ✅ Run all tests to establish baseline
5. ✅ Analyze failures and refine architecture
6. ✅ Iterate until all tests pass

## 📊 Success Metrics

Track your progress:
- [ ] All 8 tests run without errors
- [ ] At least 4 tests pass (≥70 on all metrics)
- [ ] At least 6 tests pass
- [ ] All 8 tests pass
- [ ] Average score ≥ 85 across all tests

## 🤝 Contributing

To improve this test suite:
1. Add new test cases for different patterns
2. Enhance evaluator logic
3. Add more sophisticated mocked tools
4. Improve documentation

---

**Created**: 2026-01-09  
**Version**: 1.0  
**Total Test Cases**: 8  
**Total Files**: 52  
**Estimated Setup Time**: 15-30 minutes  
**Estimated Run Time**: 5-40 minutes (depending on agent implementation)
