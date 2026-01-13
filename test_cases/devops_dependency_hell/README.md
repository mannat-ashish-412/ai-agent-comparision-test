# DevOps: The "Dependency Hell"

## Concept
Tests **Constraint Solving**. The agent must solve a 3-variable equation (A requires B, B requires C) rather than fixing errors linearly.

## Goal
The agent is asked to update `requests` to the latest version (2.0).
- Initial state: `requests==1.0`, `authlib==1.0`.
- Update `requests` to 2.0 -> Tests fail because `authlib==1.0` is incompatible.
- Naive fix: Revert `requests` to 1.0 (Failure to complete task).
- Correct fix: Update `authlib` to 2.0 as well.

## Success Criteria
- The agent ends with `requests==2.0` AND `authlib==2.0`.
- The agent does NOT revert changes.
