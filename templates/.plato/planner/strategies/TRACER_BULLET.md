---
name: tracer bullet
description: Implement the thinnest end-to-end slice first, then expand outward to cover remaining use cases and edge cases.
example: A PDF upload feature — TASK-01 accepts one hardcoded PDF and returns a hardcoded summary, subsequent tasks replace each hardcoded piece with real implementation.
---

## Task Splitting: Tracer Bullet Method

Implement the thinnest possible end-to-end slice first — one real request flowing through every layer, returning a real response. Once the tracer bullet is live and verified, expand outward to cover remaining use cases, edge cases, and error handling.

Example: a requirement adds a document upload feature. The system must accept a PDF, parse it, store it, and return a summary.

Split into tasks ordered by tracer bullet first:

- TASK-01: Tracer bullet — accept one hardcoded PDF, parse it, store it, return a hardcoded summary. No validation, no error handling, no edge cases. Just prove the pipe works end to end.
- TASK-02: Real PDF parsing — replace hardcoded content with actual parser output.
- TASK-03: Real storage — persist to database instead of memory.
- TASK-04: Real summary — replace hardcoded summary with generated output.
- TASK-05: Validation and error handling — unreadable PDF, oversized file, unsupported format.
- TASK-06: Edge cases — empty PDF, duplicate upload, concurrent uploads.

### Principles

- The first task must be end-to-end runnable. If it cannot be run and verified independently, it is not a tracer bullet.
- The first task must use the real tech stack — no mocks at the architecture level. Mocks are allowed inside unit tests only.
- Do not add validation, error handling, or edge cases to the tracer bullet task. These come later.
- Each subsequent task expands one dimension of completeness — replace one hardcoded piece, add one category of cases.
- Order tasks from core path outward. Never start with edge cases.
