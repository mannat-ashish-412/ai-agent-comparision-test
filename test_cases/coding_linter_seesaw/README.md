# Coding: The "Linter Seesaw"

## Concept
Tests **Loop Detection**. Two tools provide conflicting instructions. The agent must realize it is stuck and change strategy.

## Goal
The agent is asked to refactor code to pass the linter.
- Rule 1: Line length must be < 80.
- Rule 2: Variable declarations must be on one line.
- The initial code is a variable declaration > 80 chars.

If the agent splits the line, Rule 2 fails.
If the agent joins the line, Rule 1 fails.
This creates an infinite loop if the agent blindly follows the linter errors.

## Success Criteria
- The agent detects the loop (e.g., after 2-3 tries).
- The agent uses `disable_lint_rule` or `ask_human_help` to break out of the loop.
- Alternatively, the agent might comment on the impossibility.
