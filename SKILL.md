---
name: plato
description: Entry point for the Plato ticket workflow (designer/planner/coder role pipeline for features, fixer role pipeline for defects, under plato-workspace/tickets). Creates a new ticket workspace or reports the current state of an existing one and produces the exact `claude -p` / `claude --resume` command to run next.
disable-model-invocation: true
---

# Plato

Plato is this repo's ticket-driven development framework. Work on a Jira-style
ticket is organized under `plato-workspace/tickets/<ticket-number>/`.

## Init entry: `/plato init`

Sets up the Plato framework files in this repo (`.plato/` and
`plato-workspace/`) from the templates bundled with this skill.

### Init Flow

Reached when `/plato` is invoked with the argument `init`.

1. Copy `templates/.plato` to `.plato` at the project root.
2. Copy `templates/plato-workspace` to `plato-workspace` at the project root.
3. Determine default test paths, then confirm them with the user:
   - If the project does **not** have separate frontend and backend roots (a
     single app, no sibling `backend/` and `frontend/` directories at the
     project root), the defaults are `tests/unit` and `tests/e2e`.
   - If the project **does** have separate frontend and backend roots (e.g.
     `backend/` and `frontend/`), the defaults are `tests/unit` and
     `tests/e2e` under those roots — e.g. `backend/tests/unit`. Inspect the
     project structure to find the actual directories (look for
     `tests/unit`, `test/unit`, `<root>/tests/unit`, etc., and `tests/e2e`,
     `test/e2e`, `<root>/tests/e2e`, etc.) and use the first match for each;
     if no match is found, fall back to `tests/unit` / `tests/e2e` under the
     first detected root.
   - Ask the user to confirm both paths using `AskUserQuestion`:
     - Option A: the inferred default (label it as "Use default: <path>")
     - Option B: "Enter a custom path" (user types their own value)
4. Write the confirmed paths to `plato-workspace/project-context/SETTINGS.md`,
   creating the file if missing or updating these lines if they already
   exist:
   ```
   - unit-test-path: <value>
   - e2e-test-path: <value>
   ```

## Ticket entry: `/plato <ticket-number>`

**Ticket Types:**

Every ticket has a `type` — `feature` or `defect` — and each type moves
through its own role pipeline. Each role is run as a separate `claude` CLI
invocation with its own session, described by `.plato/<role>/<ROLE>.md`.

**Role status states:**

Each role (and each coder task) has a `status` field with one of four values:

| Status | Meaning |
|---|---|
| `TODO` | Not started yet. |
| `IN_PROGRESS` | Running right now in the background. |
| `WAITING` | Finished its current run and is waiting for the user to resume the session and interact. |
| `DONE` | Fully complete. |

### Feature

Feature tickets move through three roles, in order: **designer → planner → coder**.

#### Role → file mapping

| role | append-system-prompt-file |
|---|---|
| `designer` | `.plato/designer/DESIGNER.md` |
| `planner` | `.plato/planner/PLANNER.md` |
| `coder` | `.plato/coder/CODER.md` |

### Defect

Defect tickets move through a single role: **fixer** — diagnosis, fix, and
verification all happen in one session, with no separate design/planning phase.

#### Role → file mapping

| role | append-system-prompt-file |
|---|---|
| `fixer` | `.plato/fixer/FIXER.md` |

### Execute Steps

#### Step 1 — Resolve the ticket number

If the skill was invoked with an argument, that's the ticket number. If not,
ask the user: "What is the ticket number?" and wait for the answer.

#### Step 2 — New or existing?

If `plato-workspace/tickets/` doesn't exist yet (first-ever ticket in this
repo), create it before checking further.

Check whether `plato-workspace/tickets/<ticket-number>/status.json` exists.

- Does not exist → go to Step 3a (new)
- Exists → go to Step 3b (existing)

#### Step 3a — New: determine ticket type, then create

Ask the ticket type. Use `AskUserQuestion` with two options: `feature` and
`defect`. Then:

- `feature` → **Feature Creation Flow**: See `references/FEATURE_CREATION_FLOW.md`.
- `defect` → **Defect Creation Flow**: See `references/DEFECT_CREATION_FLOW.md`.

#### Step 3b — Existing: read ticket type, then continue

Read the `type` field from `plato-workspace/tickets/<ticket-number>/status.json`. Then:

- `feature` → **Feature Continue Flow**: See `references/FEATURE_CONTINUE_FLOW.md`.
- `defect` → **Defect Continue Flow**: See `references/DEFECT_CONTINUE_FLOW.md`.
