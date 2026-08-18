# Initialize

```
/plato init
```

Copies `.plato/` (role ABS files + status CLI) and `plato-workspace/`
(tickets, project-context, role-rules) into your project root, then asks
you to confirm your unit-test and e2e-test paths.

# Overview

## Ticket types

Every unit of work in Plato is a **ticket**, tracked under
`plato-workspace/tickets/<ticket-number>/status.json`. A ticket has exactly
one `type`, and the type decides which roles it moves through:

- **feature** — new functionality, described by a `REQUIREMENT.md` (user
  story + acceptance criteria), worked by the full **designer → planner →
  coder** pipeline.
- **defect** — a bug, described by a `DEFECT.md` (description + repro
  steps), worked by the single **fixer** role.

You pick the type once, when you create the ticket with `/plato
<ticket-number>`

## Roles

A **role** is one step of a ticket's pipeline — `designer`, `planner`,
`coder`, or `fixer`. Each role runs as its own independent claude code session, so it starts with a clean context every time and can be resumed
later with `claude --resume <session-id>`.

Every role (and every coder task) carries a `status`:

| Status | Meaning |
|---|---|
| `TODO` | Not started yet. |
| `IN_PROGRESS` | Running right now. |
| `WAITING` | Finished its current run and is waiting for you to resume and respond. |
| `DONE` | Fully complete. |

You never run `claude` by hand to move a ticket forward — `/plato
<ticket-number>` always tells you the exact command to run next, based on
this status.

### Feature roles

Feature tickets move through three roles, strictly in order:

1. **designer** — reads `REQUIREMENT.md`, interviews you with clarifying
   questions, and produces `DESIGN.md` plus a Design Review (`.dr.md`) for
   you to approve or reject.
2. **planner** — reads `DESIGN.md` and breaks it into `tasks.json`,
   presented as a Tasks Review (`.tr.md`).
3. **coder** — implements `tasks.json` one task at a time. Each task
   produces its own Commit Request (`.cr.md`) that you review and approve
   before the next task starts.

You can't skip ahead — planner won't run until designer is `DONE`, and each
coder task waits for the previous one to be approved.

### Defect roles

Defect tickets move through a single role:

- **fixer** — reads `DEFECT.md`, reproduces the bug, and presents you with
  the root cause *before* writing any fix. Once you confirm the root cause,
  it implements the fix and produces a Fix Request (`.fr.md`) for review.

There's no separate design or planning phase for defects — diagnosis, fix,
and verification all happen in this one session.

## Folders

`/plato init` creates two top-level folders in your project. Together they
are the whole framework — everything else is generated per ticket.

### .plato

The rulebook. This is what governs *how* each role behaves:

- `designer/DESIGNER.md`, `planner/PLANNER.md`, `coder/CODER.md`,
  `fixer/FIXER.md` — the ABR (Agent Behavior Rules) file for each role,
  appended as the system prompt when that role's session starts.
- `*_REQUEST.md` files next to each role's ABR — the commit-lock rule
  files. See [`04-commit-lock.md`](04-commit-lock.md) for details, but you
  don't need to dig into this yet.

### plato-workspace

Where the actual work lives:

- `project-context/` — files loaded into every role's context regardless of
  ticket, e.g. `SETTINGS.md` (your unit-test/e2e-test paths). This is where
  you organize your project's own knowledge as `.md` files. The rule:
  anything every agent must know goes in `INDEX.md`'s **must know**
  section; everything else goes into subfolders, indexed from `INDEX.md`,
  so agents don't load more context than they need.
- `role-rules/<role>/` — living rule files per role (e.g. `NEVER.md`,
  `MATRIX_SPLIT.md`), loaded into that role's context on every run.
- `tickets/<ticket-number>/` — one folder per ticket, created on demand.
  Holds `status.json`, plus the ticket's requirement/design/review files,
  etc.

### .plato vs plato-workspace

The core difference: `.plato` is **static** — it's part of the framework's
own source, and you'll rarely need to touch it. `plato-workspace` is
**dynamic** — it's the content that keeps growing and evolving as you
actually work the project.

---

**Next:** [02. Prepare workspace →](02-prepare.md)
