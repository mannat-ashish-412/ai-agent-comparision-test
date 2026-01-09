# Test Case 4: Planner-Workers-Join

## Overview
Tests decomposition, parallel execution, and merging pattern.

## Scenario
Create MongoDB → DynamoDB migration plan by decomposing into 3 subtasks.

## Multi-Agent Requirements
1. **Planner**: Decompose into subtasks
2. **Workers**: Execute subtasks in parallel
3. **Joiner**: Merge results
4. **Validator**: Check consistency

## Why Single Agent Fails
Single agents produce plans with internal contradictions between sections.

## Pass Criteria
All scores ≥ 70
