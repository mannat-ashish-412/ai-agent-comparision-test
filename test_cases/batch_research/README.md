# Test Case 8: Batch Knowledge Base Research

## Overview
Tests parallel retrieval and synthesis with proper citation tracking.

## Scenario
Answer 5 questions about company policies using KB snippets.

## Multi-Agent Requirements
1. **Worker Agents**: Retrieve answers in parallel
2. **Synthesizer**: Unify answers with citations

## Why Single Agent Fails
Single agents serialize calls and lose attribution of which snippet answered which question.

## Pass Criteria
All scores ≥ 70, all 5 answers must cite KB source
