# Test Case 5: RCA + Fix + Regression Tests

## Overview
Tests separation of diagnosis, fix, and testing roles.

## Scenario
Failing CI test due to email validation rejecting '+' character.

## Multi-Agent Requirements
1. **Debugger**: Identify root cause
2. **Fixer**: Propose patch
3. **Tester**: Write regression tests

## Why Single Agent Fails
Mixes diagnosis and solution, leading to hallucinated fixes.

## Pass Criteria
All scores ≥ 70
