<div align="center">
  <img src="assets/plato-logo-brass-transparent.png" alt="Plato logo" width="200">
</div>

# Plato

*Built for engineers who get tickets, not greenfield projects.*

> **⚠️ Warning: if you are not a professional engineer, Plato is not for
> you.** It assumes you're a software engineer with years of hands-on
> experience, comfortable with Jira, Scrum, git, and professional software
> project workflows in general. If that's not you, look at fully-automated
> tools like Superpowers or GSD instead.

Plato is an AI coding methodology framework for Claude Code. It is designed
around how real engineers on real teams actually work: you get a ticket not an
open-ended mandate to build something from scratch. 

Plato organizes the whole lifecycle of that ticket, from requirement to reviewed diff, as a
sequence of small, transparent, human-checkpointed AI sessions.

## Philosophy

### Framework, not platform

Plato is deliberately a **framework** (like Spring or React), not a
**platform** (like a low-code tool or a fully automated agent runner). It
gives you conventions, scaffolding, and best practices — it does not
generate your design for you, run agents unsupervised, or make decisions on
your behalf. Every step is visible and stays under your control.

| | GSD | Superpowers | Plato |
|---|---|---|---|
| Type | Platform | Plugin system | Framework |
| Transparency | Low (black box) | Medium | High (white box) |
| Target user | Solo developer | General developer | Team engineer |
| State management | In-memory (TodoWrite) | In-memory | File-based (persistent) |
| Session model | Long sessions | Long sessions | Short `-p` sessions |
| ABS generation | Automated | Automated | Manual (engineer writes) |

### ABS — Agent Behavior Specification

Each role in the pipeline (`designer`, `planner`, `coder`, `fixer`) is
governed by a single `.md` file — its **ABS**, analogous to an HDL
description in electronics: it specifies *how the agent should behave*, not
*what business logic to implement*. `DESIGNER.md`, `PLANNER.md`, `CODER.md`,
`FIXER.md` are the human's primary artifact in this framework — you own and
edit these, the model owns the source code it produces from them.

### Human as legislator, model as executor

You write the rules (ABS files, role-rules); the model executes tasks
against them and produces code. You never write application code by hand in
this workflow — you write and refine the rules that govern how the code
gets written, and you review every output before it's accepted.

### Transparency over automation

Every role runs as its own independent `claude -p --session-id <uuid>`
process, resumable at any time with `claude --resume <session-id>`. All
state lives in plain files — `status.json`, `tasks.json`, `DESIGN.md`,
`REQUIREMENT.md` / `DEFECT.md` — so nothing is hidden in an opaque agent
loop.

### Short sessions, no context rot

Each role starts a fresh session and ends when its step is done. This
avoids context dilution (rules buried under noise), context corruption, and
context rot from long-running sessions drifting away from their original
instructions.

### CR as audit trail

Every code change produces a structured **Change/Commit/Fix Request**
(CR/TR/DR/FR — see below) before it's approved: what changed, why, how it
was verified. It's your checkpoint to approve, reject, or interrogate the
change, and it stays in the ticket folder as an audit trail until approved.

## Ticket pipelines

Every ticket has a `type` and moves through its own fixed pipeline of
roles. Each role is a separate `claude -p` invocation, driven by its ABS
file under `.plato/<role>/<ROLE>.md`.

```
feature ticket:  designer  →  planner  →  coder (per task)
defect ticket:   fixer  (diagnosis + fix + verification, one session)
```

**Feature** — `designer` turns `REQUIREMENT.md` into `DESIGN.md` (via a
clarifying-question interview + a Design Review, `.dr.md`); `planner` turns
`DESIGN.md` into `tasks.json` (via a Tasks Review, `.tr.md`), splitting work
using the matrix-splitting method (tech-stack columns × business-domain
rows, see `templates/plato-workspace/role-rules/planner/MATRIX_SPLIT.md`);
`coder` implements each task one at a time, producing a Commit Request
(`.cr.md`) per task for you to review and approve.

**Defect** — `fixer` reproduces the bug from `DEFECT.md`, presents the root
cause for your confirmation *before* touching any code, implements the fix,
and produces a Fix Request (`.fr.md`) for review.

Every role/task has a status:

| Status | Meaning |
|---|---|
| `TODO` | Not started yet. |
| `IN_PROGRESS` | Running right now in the background. |
| `WAITING` | Finished its run, waiting for you to resume and respond. |
| `DONE` | Fully complete. |

Approving a review is gated: for coder/fixer, you must have asked at least
3 questions about the generated code during the Q&A step before `approve`
is accepted — this exists to force real review instead of rubber-stamping.
Any new rule surfaced during review (`New Rules` section of a CR/DR/TR/FR)
gets appended to that role's rule file under
`plato-workspace/role-rules/<role>/`, so the framework's behavior for this
project improves ticket over ticket.

**Plato never runs `git commit` or `git push` on your behalf, for any
role.** You review and commit manually, always.

## Installation

This repository *is* a Claude Code Skill named `plato`. Install it with the
[skills CLI](https://github.com/anthropics/skills):

```
npx skills@latest add CodePlato3721/plato -y -g
```

This fetches the skill into your global skills directory, making `/plato`
available in Claude Code. All of `SKILL.md`'s own paths (`references/`,
`scripts/`, `templates/`) are relative to the skill's own directory, so it
works the same wherever the skills CLI installs it.

## Usage

### 1. Initialize the framework in your project

```
/plato init
```

Copies `.plato/` (role ABS files + status CLI) and `plato-workspace/`
(tickets, project-context, role-rules) into your project root, then asks
you to confirm your unit-test and e2e-test paths.

### 2. Work a ticket

```
/plato <ticket-number>
```

- **New ticket**: asks the ticket type (`feature`/`defect`) and title,
  scaffolds `plato-workspace/tickets/<ticket-number>/`, and gives you the
  exact `claude -p --session-id ... --append-system-prompt-file ...`
  command to run for the first role. Fill in `REQUIREMENT.md` (feature) or
  `DEFECT.md` (defect) before starting.
- **Existing ticket**: reports current status (`status_report.py`), finds
  the active role/task (`find_active_step.py`), and prints the right
  command to either start the next step or resume the session that's
  waiting on you (`generate_command.py`).

Each generated command is a standalone `claude -p` invocation with its own
`--session-id`, so every step of the pipeline is independently resumable
and auditable.

## Repository layout

```
plato/
├── SKILL.md                     entry point: /plato init, /plato <ticket-number>
├── references/                  flow docs the skill dispatches to
│   ├── FEATURE_CREATION_FLOW.md
│   ├── FEATURE_CONTINUE_FLOW.md
│   ├── DEFECT_CREATION_FLOW.md
│   └── DEFECT_CONTINUE_FLOW.md
├── scripts/                     helper CLIs the skill shells out to
│   ├── generate_command.py      builds the next `claude -p` / `--resume` command
│   ├── status_report.py         renders a ticket's status.json as a report
│   ├── find_active_step.py      finds the active role/task for a ticket
│   ├── roles/                   per-role command-building strategies
│   ├── status/                  status.json read helpers
│   └── tasks/                   tasks.json read helpers
└── templates/                   scaffolding copied into a project by `/plato init`
    ├── .plato/                  → becomes `<project>/.plato/`
    │   ├── designer/DESIGNER.md, DESIGN_REQUEST.md
    │   ├── planner/PLANNER.md, TASKS_REQUEST.md, tasks.template.json
    │   ├── coder/CODER.md, COMMIT_REQUEST.md
    │   ├── fixer/FIXER.md, FIX_REQUEST.md
    │   └── scripts/status_cli.py   updates status.json (run/wait/approve/reject)
    ├── plato-workspace/         → becomes `<project>/plato-workspace/`
    │   ├── project-context/SETTINGS.md   test path config, shared project context
    │   ├── role-rules/<role>/NEVER.md    living, per-role rule files (grow via review)
    │   └── tickets/                      one folder per ticket, created on demand
    └── ticket/                  default status.json shapes for feature/defect tickets
```

## Inspiration

- **[Superpowers](https://github.com/obra)** (obra) — skill-based workflow
  methodology; Plato borrows the concept of role-specific ABS files.
- **GSD** — file-based state management; Plato keeps the persistent-state
  idea but avoids the platform complexity.
- **Spring / React** — the framework philosophy of providing conventions
  and scaffolding, not business logic.
