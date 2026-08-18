---
name: vertical slice
description: Split by business domain, each task delivers a complete working slice through all tech stack layers.
example: A badge appearing on Dashboard, Settings, and Billing — 3 domains, 3 tasks, each end-to-end complete.
---

## Task Splitting: Vertical Slice Method

Use the vertical slice method. Each task delivers a complete, working slice of functionality that cuts through all tech stack layers — from DAO to Service to View — within a single business domain.

Example: a requirement adds a VIP membership badge to the system. The badge must appear on 3 pages — Dashboard, Account Settings, and Billing. These are 3 business domains.

Each business domain becomes one task. Each task implements the full stack for that domain:

- TASK-01: VIP badge — Dashboard (DAO + Service + View)
- TASK-02: VIP badge — Account Settings (DAO + Service + View)
- TASK-03: VIP badge — Billing (DAO + Service + View)

Each task is independently runnable and testable when complete.

### Principles

- Split by business domain, not by tech stack layer.
- Each task must be end-to-end complete — it touches every layer it needs to function.
- Each task must be independently testable without depending on another task being done first.
- Do not create tasks like "implement DAO layer" or "implement Service layer" — these are not vertical slices.
- If a task requires shared infrastructure (e.g. a base DAO class), extract it as a prerequisite task and mark it explicitly as a dependency.