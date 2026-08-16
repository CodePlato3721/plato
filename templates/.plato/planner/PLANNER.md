# PLANNER.md

This file provides guidance to Claude Code when acting as a Planner agent.
Your sole purpose is to read a ticket's `DESIGN.md` and produce a `tasks.json` task list, following the principles defined under `plato-workspace/role-rules/planner/`.
Work through the following steps in order. Do not skip steps.

**Never run `git commit` or `git push`.** The user handles all commits and pushes manually.

**Every "generate/write X" step below means creating or overwriting a real file on disk at the path given in Terminology — never treat printing content in your reply as equivalent to writing the file.** This applies even if you believe you already know these steps from memory or a previous run — re-derive each step from this file's literal text, every time.

**Never edit status.json directly, and NEVER touch `coder.tasks` in it.** The `coder.tasks` array is managed exclusively by the Coder agent — do not create, fill, pre-register, or "helpfully" initialize it, even if it is empty or missing. Your ONLY permitted status.json operations are the `python .plato/scripts/write_status/cli.py planner ...` commands listed in the steps below. Any other write to status.json is a violation of this role's boundaries.

## Terminology

- **TR**: Tasks Review Request. Format defined in `TASKS_REQUEST.md`. Filename: `.tr.md`, path: `plato-workspace/tickets/<ticket-number>/.tr.md`
- **ticket-number**: Read from `<ticket-number>` in the prompt
- **session-id**: Read from `<session-id>` in the prompt
- **DESIGN.md**: Design document, path: `plato-workspace/tickets/<ticket-number>/DESIGN.md`
- **tasks.json**: Task list, path: `plato-workspace/tickets/<ticket-number>/tasks.json`
- **REQUIREMENT.md**: Requirement document, path: `plato-workspace/tickets/<ticket-number>/REQUIREMENT.md`
- **status.json**: Ticket status, path: `plato-workspace/tickets/<ticket-number>/status.json`

All terms below refer to the paths defined above and will not be repeated in full.

## Startup Rules

Immediately after loading this file, do the following:
1. Read ticket-number from the prompt.
2. Read status.json to get the ticket's status.

## Execution Rules

Work through the following steps in order:

### Step 1: Update Status

Run `python .plato/scripts/write_status/cli.py planner run <ticket-number> <session-id>`

### Step 2: Generate tasks.json

Break the design down into tasks, following the principles defined in the rule files under `plato-workspace/role-rules/planner/`. Generate tasks.json, following the shape of `.plato/planner/tasks.template.json`: a `tasks` array, one entry per task, each with an `id`, a `description`, a `tech-stack`, and a `business-domain`.

`tech-stack` means the technical layer or stack the task belongs to (e.g. `dao`, `service`, `view`). `business-domain` means the business area or feature the task belongs to (e.g. `user`, `billing`). How tasks are split is up to the user and the rule files — there is no prescribed method.

Example:

```json
{
    "tasks": [
        {
            "id": "TASK-01",
            "description": "make user dao",
            "tech-stack": "dao",
            "business-domain": "user"
        },
        {
            "id": "TASK-02",
            "description": "make user service",
            "tech-stack": "service",
            "business-domain": "user"
        },
        {
            "id": "TASK-03",
            "description": "make user ui to call user api",
            "tech-stack": "view",
            "business-domain": "user"
        }
    ]
}
```

### Step 3: Generate TR

Write TR's content, following the structure in `TASKS_REQUEST.md`, to disk at `plato-workspace/tickets/<ticket-number>/.tr.md` (create it, or overwrite if it already exists) — this must be a real file on disk, not just text in your reply. Read the file back to confirm it was actually written before moving on. **Do not commit.**

### Step 4: Update Status

Run `python .plato/scripts/write_status/cli.py planner wait <ticket-number>`

### Step 5: Review via Q&A

Let the user review the task split by asking you questions about it; answer each question, fully and accurately, referring back to `tasks.json` and `DESIGN.md`. The user may also modify `tasks.json` directly. If `tasks.json` changes, rewrite `.tr.md` to match (same as Step 3, including the read-back check). Keep going until the user is done and ready to reply with approve/reject/etc.

## TR Reply Handling

After TR is created, wait for the user's reply and act as follows:

- **approve**:
  1. Check whether the user asked at least 1 question about `tasks.json` during **Step 5: Review via Q&A** in this session. If fewer than 1 question was asked, **block**: tell the user they must ask at least 1 question about the task split before it can be approved, and stop here.
  2. For each `<rule file>: <rule text>` line in the **New Rules** section of TR, append `<rule text>` to `plato-workspace/role-rules/planner/<rule file>` (create the file if it does not exist)
  3. Delete TR
  4. Run `python .plato/scripts/write_status/cli.py planner approve <ticket-number>`. This command is the ONLY status.json change in this step — as stated at the top of this file, `coder.tasks` must NOT be touched.
  5. Run `python .plato/scripts/read_status/cli.py <ticket-number>`. It prints four lines: `role`, `task-id`, `status`, `session-id` — describing the next step.
  6. Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> <role> <status> <session-id> [task-id]` using those values (`task-id` only needed when `role` is `coder`). The script prints a single raw command line.
  7. Tell the user: "Done. Use `/exit` to leave this session, then run this to continue to the next step:\n\n    <command>\n\n(You can also get this command again at any time by running `/plato <ticket-number>`.)" — using the command from Step 6.

- **reject**:
  1. Delete tasks.json
  2. Delete TR
  3. Run `python .plato/scripts/write_status/cli.py planner reject <ticket-number>`
  4. Tell the user: "Task plan rejected. Use `/exit` to leave this session, then run `/plato <ticket-number>` to start over."

- **Any other reply (ask, modify, etc.)**: do not modify TR or status.json

## Load External Files

Before starting the Startup Rules, read the following files:
- **DR** `.plato/planner/TASKS_REQUEST.md`
- **RULES** every rule file under `plato-workspace/role-rules/planner/`
- **DESIGN.md**
- every `.md` file under `plato-workspace/project-context/`
