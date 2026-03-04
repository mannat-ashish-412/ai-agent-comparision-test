# EntraID Roles Update Test Case

## Description
This test case evaluates the agent's ability to interpret unstructured text instructions for Role Based Access Control (RBAC) and apply them to a user database.

## Scenario
The agent acts as an identity administrator. It must:
1.  Read a list of users.
2.  Parse unstructured text from HR/IT detailing role changes.
3.  Update each user's roles using an API that returns a Request ID.
4.  Verify the status of each Request ID to ensure the update was successful.

## Goals
- **Interpretation**: Correctly map "Sarah needs Admin" to adding the Admin role.
- **Tools Usage**: Call `update_user_roles` for each user and `verify_request_status` for each request.
- **Verification**: Ensure no request is left unverified.

## Evaluation
The simulated DB is checked to ensure the final roles match the ground truth derived from the instructions.
