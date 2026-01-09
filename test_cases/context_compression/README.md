# Test Case 7: Long Context Compression

## Overview
Tests ability to compress long conversation history and solve from compressed state.

## Scenario
30-message conversation about microservice deployment with a key change (PostgreSQL → RDS).

## Multi-Agent Requirements
1. **Summarizer**: Compress history into stable state
2. **Solver**: Answer question using only compressed state

## Why Single Agent Fails
Single agents get brittle with long histories, miss updates.

## Pass Criteria
All scores ≥ 70, must use RDS (not self-managed PostgreSQL)
