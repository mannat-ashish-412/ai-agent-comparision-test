# Application Security: The "Blind Patcher"

## Concept
Tests **Confirmation Bias**. A single agent cannot effectively "Red Team" (attack) the code it just "Blue Teamed" (built).

## Goal
The agent must fix an XSS vulnerability in a simple function. The catch is that there is a "trap" in the verification tool:
- `verify_security("standard")` returns `SAFE`.
- `verify_security("polyglot")` returns `VULNERABLE`.

A standard agent will likely apply a simple fix, check "standard", see "SAFE", and declare victory.
A robust multi-agent (or red-teaming) setup should verify with advanced payloads ("polyglot") and catch the failure.

## Success Criteria
- The agent must explicitly test with `"polyglot"` payloads.
- The agent must use a proper HTML sanitization library (e.g., `bleach`, `html.escape`) instead of brittle regex or string replacement.
