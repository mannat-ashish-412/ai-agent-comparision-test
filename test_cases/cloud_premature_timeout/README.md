# Cloud: The "Premature Timeout"

## Concept
Tests **Async State Handling**. The agent must handle "Eventual Consistency" (waiting for a resource) without crashing or duplicating requests.

## Goal
The agent must provision a database and then create a table.
- `create_db` starts the process but returns "CREATING".
- `create_table` fails if status is "CREATING".
- `get_db_status` returns "CREATING" for the first 3 calls, then "AVAILABLE".

A naive agent might try to create the table immediately and fail, or try to `create_db` again thinking it failed.
A good agent will `create_db`, then enter a loop: `wait` -> `get_db_status` -> check if AVAILABLE -> loop or break.

## Success Criteria
- The agent successfully creates the table.
- The agent does NOT call `create_db` multiple times.
- The agent uses the `wait` tool.
