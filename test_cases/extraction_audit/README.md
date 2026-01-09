# Test Case 2: Extraction and Consistency Audit

## Overview
This test evaluates the system's ability to extract structured requirements from messy text and audit them for contradictions using separate specialized agents.

## Scenario
Process a requirements document for an e-commerce checkout system that contains 9 deliberate contradictions across:
- Authentication (login vs guest checkout)
- Payment processing (timing and storage)
- Shipping costs
- Inventory management (cart reservation and overselling)
- Order confirmation (tracking and SMS)
- Return policies

## Multi-Agent Requirements
This test requires role separation:

1. **Extractor Agent**: Parse unstructured text into structured PRD
2. **Auditor Agent**: Identify contradictions and inconsistencies
3. **Clarification Agent**: Generate questions for unresolved conflicts

## Why Single Agent Fails
A single agent typically:
- Overfits to one interpretation, ignoring contradictions
- Produces PRD that glosses over conflicts
- Fails to maintain separation between extraction and validation
- Misses subtle contradictions due to confirmation bias

## Expected Behavior
The multi-agent system should:
- Extract complete PRD with all 6 sections
- Identify at least 6 of 9 contradictions
- Generate exactly 3 clarifying questions
- Provide resolution status for each contradiction
- Show clear agent attribution

## Pass Criteria
- **Correctness ≥ 70**: Complete PRD structure, contradictions identified, questions generated
- **Consistency ≥ 70**: Audit findings match PRD content
- **Conflict Handling ≥ 70**: Contradictions explicitly flagged with details
- **Traceability ≥ 70**: Clear separation between extractor and auditor roles

## Time Limit
5 minutes

## Files
- `config.json` - Test configuration with prompts
- `input_data.json` - Requirements document with contradictions
- `expected_output.json` - Expected contradictions and structure
- `mocked_tools.py` - Extraction, contradiction detection, and validation tools
- `evaluator.py` - Custom scoring logic
