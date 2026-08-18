---
name: plato
description: Entry point for the Plato ticket workflow (designer/coder role pipeline for simple features, designer/planner/coder for complex features, fixer role pipeline for defects, under plato-workspace/tickets). Creates a new ticket workspace or reports the current state of an existing one and produces the exact `claude` / `claude --resume` command to run next.
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
2. Add `.plato/` to `.gitignore` at the project root (create the file if
   missing; append the line only if it isn't already present).
3. Copy `templates/plato-workspace` to `plato-workspace` at the project root.
4. Determine the project's roots:
   - If the project does **not** have separate frontend and backend roots (a
     single app, no sibling `backend/` and `frontend/` directories at the
     project root), there is a single root: the project root itself.
   - If the project **does** have separate frontend and backend roots (e.g.
     `backend/` and `frontend/`), there are two roots, named after those
     directories.
5. For **each** root from step 4, independently determine default test paths
   and confirm them with the user:
   - Search **only inside that root** (look for `tests/unit`, `test/unit`,
     `<root>/tests/unit`, etc., and `tests/e2e`, `test/e2e`,
     `<root>/tests/e2e`, etc.) for a unit-test default and an e2e-test
     default. If no match is found under that root, fall back to
     `tests/unit` / `tests/e2e` under that root. Never reuse a match found
     under a different root.
   - Ask the user to confirm both paths for this root using
     `AskUserQuestion`:
     - Option A: the inferred default (label it as "Use default: <path>")
     - Option B: "Enter a custom path" (user types their own value)
6. Write the confirmed paths to `plato-workspace/project-context/SETTINGS.md`,
   creating the file if missing:
   - **Single root**: write a flat pair, no header, updating these lines if
     they already exist:
     ```
     - unit-test-path: <value>
     - e2e-test-path: <value>
     ```
   - **Multiple roots**: write one `#`-headed section per root, named after
     the root directory, updating each section's lines if it already
     exists:
     ```
     # backend

     - unit-test-path: <value>
     - e2e-test-path: <value>

     # frontend

     - unit-test-path: <value>
     - e2e-test-path: <value>
     ```

## Upgrade entry: `/plato upgrade`

Refreshes this project's `.plato/` with the version bundled in this skill,
without touching `plato-workspace/`.

### Upgrade Flow

Reached when `/plato` is invoked with the argument `upgrade`.

1. If `.plato` does not exist at the project root, tell the user to run
   `/plato init` instead and stop.
2. Overwrite `.plato` at the project root with `templates/.plato` (delete
   files that no longer exist in the template, add new ones, replace
   changed ones). Do **not** touch `plato-workspace/` in any way.
3. Tell the user the upgrade is done. `.plato` is gitignored, static
   framework source regenerated from this skill's templates — any local
   edits to it are not tracked by git and would be silently overwritten.

## Ticket entry: `/plato <ticket-number>`

**Ticket Types:**

Every ticket has a `type` — `simple_feature`, `complex_feature`, or `defect`
— and each type moves through its own role pipeline. Each role is run as a
separate `claude` CLI invocation with its own session, described by
`.plato/<role>/<ROLE>.md`.

**Role status states:**

Each role (and each coder task) has a `status` field with one of four values:

| Status | Meaning |
|---|---|
| `TODO` | Not started yet. |
| `IN_PROGRESS` | Running right now. |
| `WAITING` | Finished its current run and is waiting for the user to resume the session and interact. |
| `DONE` | Fully complete. |

### Simple Feature

Simple feature tickets move through two roles, in order: **designer → coder**.
No planner step, and `coder` is a single role entry (not a task list) —
there's no task-by-task breakdown.

#### Role → file mapping

| role | append-system-prompt-file |
|---|---|
| `designer` | `.plato/designer/DESIGNER.md` |
| `coder` | `.plato/coder/CODER.md` |

### Complex Feature

Complex feature tickets move through three roles, in order: **designer → planner → coder**.
The planner breaks the design into small tasks, and `coder` works through
`coder.tasks[]` one task at a time.

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
`defect`.

If `feature`, ask a follow-up question with `AskUserQuestion`: whether it's a
**simple feature** or a **complex feature**. Explain the difference — a
complex feature enables the planner role, which breaks the design down into
small tasks executed one at a time; a simple feature skips planning and goes
straight from design to a single coder pass. Then:

- `simple feature` → **Simple Feature Creation Flow**: See `references/SIMPLE_FEATURE_CREATION_FLOW.md`.
- `complex feature` → **Complex Feature Creation Flow**: See `references/COMPLEX_FEATURE_CREATION_FLOW.md`.
- `defect` → **Defect Creation Flow**: See `references/DEFECT_CREATION_FLOW.md`.

#### Step 3b — Existing: read ticket type, then continue

Read the `type` field from `plato-workspace/tickets/<ticket-number>/status.json`. Then check whether the ticket's work is already finished:

- `defect`: `fixer.status` is `DONE`
- `complex_feature`: `coder.tasks` is non-empty and every task's `status` is `DONE`
- `simple_feature`: `coder.status` is `DONE`

If finished, go to **Finish Flow**: See `references/FINISH_FLOW.md` — shared by all ticket types.

Otherwise:

- `simple_feature` → **Simple Feature Continue Flow**: See `references/SIMPLE_FEATURE_CONTINUE_FLOW.md`.
- `complex_feature` → **Complex Feature Continue Flow**: See `references/COMPLEX_FEATURE_CONTINUE_FLOW.md`.
- `defect` → **Defect Continue Flow**: See `references/DEFECT_CONTINUE_FLOW.md`.
