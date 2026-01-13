# Multi-Agent Workflow Test Suite - Advanced Edition

## 📋 What Has Been Created

A set of **5 Advanced Test Cases** designed to be rigorous "Agent Breakers" that a standard single-agent setup will statistically fail, justifying the move to a Multi-Agent architecture.

## 📁 Directory Structure

```
test_cases/
├── app_security_blind_patcher/    # Test Case 1: App Security
├── pentesting_rabbit_hole/        # Test Case 2: Pentesting
├── coding_linter_seesaw/          # Test Case 3: Coding
├── cloud_premature_timeout/       # Test Case 4: Cloud
└── devops_dependency_hell/        # Test Case 5: DevOps
```

## 🎯 Test Cases Overview

### 1. Application Security: The "Blind Patcher"
- **Concept**: Tests **Confirmation Bias**.
- **Challenge**: Fix an XSS vulnerability where `verify_security("standard")` returns SAFE but `verify_security("polyglot")` returns VULNERABLE.
- **Why Single Agent Fails**: Only checks the standard case and declares victory prematurely.

### 2. Pentesting: The "Rabbit Hole"
- **Concept**: Tests **Context Window Management**.
- **Challenge**: Find the Critical RCE (EternalBlue) amidst 5000 lines of directory brute-force noise.
- **Why Single Agent Fails**: Gets processing the noise and misses the critical signal.

### 3. Coding: The "Linter Seesaw"
- **Concept**: Tests **Loop Detection**.
- **Challenge**: Refactor code where two linter rules contradict each other (Line length vs Variable on one line).
- **Why Single Agent Fails**: Oscillates infinitely between fixing one error and causing the other.

### 4. Cloud: The "Premature Timeout"
- **Concept**: Tests **Async State Handling**.
- **Challenge**: Provision a DB (which takes time) before creating a table.
- **Why Single Agent Fails**: Fails to wait for "AVAILABLE" status and errors out on table creation.

### 5. DevOps: The "Dependency Hell"
- **Concept**: Tests **Constraint Solving**.
- **Challenge**: Update `requests` to 2.0, which breaks `authlib` 1.0. Must update `authlib` too, not revert `requests`.
- **Why Single Agent Fails**: Linear error fixing leads to reverting the initial change (giving up).

## 📊 Evaluation
Each test case comes with an `evaluator.py` that uses an LLM Judge to score:
- **Correctness**
- **Consistency**
- **Conflict Handling**
- **Traceability**
