# Test Case 3: Tool Output Conflict Resolution

## Overview
Tests the system's ability to detect and resolve conflicting data from multiple sources with explicit adjudication.

## Scenario
Query product pricing from three sources that return conflicting values:
- Pricing API: ₹999 (most recent, 2 hours ago)
- Catalog DB: ₹1,099 (older, 1 day ago)  
- Cache: ₹999 (30 minutes ago)

## Multi-Agent Requirements
1. **Data Collector**: Query all sources
2. **Conflict Detector**: Identify discrepancies
3. **Arbitrator**: Apply resolution policy
4. **Auditor**: Document decision trail

## Why Single Agent Fails
Single agents often silently pick one value without acknowledging conflicts or providing reasoning.

## Expected Behavior
- Detect conflict between API (₹999) and DB (₹1,099)
- Apply resolution policy (freshness → API, authority → API, consensus → ₹999)
- Provide complete audit trail

## Pass Criteria
All scores ≥ 70

## Files
- `config.json`, `input_data.json`, `expected_output.json`
- `mocked_tools.py` - Tools returning conflicting prices
- `evaluator.py` - Scoring logic
