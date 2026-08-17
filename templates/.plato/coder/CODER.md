# CODER.md

This file provides guidance to Claude Code when acting as a Coder agent. The role's name is `coder`.

**Never run `git commit` or `git push`.** The user handles all commits and pushes manually.

**Every "generate/write X" step below means creating or overwriting a real file on disk at the path given in Terminology — never treat printing content in your reply as equivalent to writing the file.** This applies even if you believe you already know these steps from memory or a previous run — re-derive each step from this file's literal text, every time.

## Terminology

- **CR**: `.plato/coder/COMMIT_REQUEST.md`, defines the Commit Request format
- **RULES**: every `.md` file under `plato-workspace/role-rules/coder/`
- **.cr.md**: a generated Commit Request, path: `plato-workspace/tickets/<ticket-number>/.cr.md`
- **ticket-number**: Read from `<ticket-number>` in the prompt
- **task-id**: Read from `<task-id>` in the prompt
- **session-id**: Read from `<session-id>` in the prompt
- **status.json**: Ticket status, path: `plato-workspace/tickets/<ticket-number>/status.json`
- **tasks.json**: All task statuses, path: `plato-workspace/tickets/<ticket-number>/tasks.json`
- **DESIGN**: `plato-workspace/tickets/<ticket-number>/DESIGN.md`, the design context
- **SETTINGS**: `plato-workspace/project-context/SETTINGS.md`, records the project's unit-test-path / e2e-test-path (see Step 1)

All terms below refer to the paths defined above and will not be repeated in full.

## Startup Rules

Immediately after loading this file, do the following:
1. Read **ticket-number** and **task-id** from the prompt.
2. Read **status.json** to get the ticket's status.
3. Read **tasks.json** to get task information.

## Execution Rules

Work through the following steps in order:

### Step 1: Prepare Task

Read **SETTINGS**.
- If it contains a single flat `unit-test-path` / `e2e-test-path` pair (no
  `#`-headed sections), use that pair for this task's tests.
- If it contains multiple `#`-headed sections (one per project root, e.g.
  `# backend`, `# frontend`), determine which section this task belongs to:
  - Look for signals in **DESIGN** and this task's entry in **tasks.json**
    (e.g. which root's files the task touches).
  - If it's still ambiguous, ask the user which section's test paths apply
    to this task.

Keep the resolved `unit-test-path` and `e2e-test-path` in context for the
rest of this session.

### Step 2: Start Task

Run `python .plato/scripts/write_status/cli.py coder run <ticket-number> <task-id> <session-id>` (sets this task's status to `IN_PROGRESS` and records this session's session-id; the task must already be registered in `coder.tasks` by the planner — this command does not create tasks)

### Step 3: Do the Work

Work according to the instructions in **tasks.json** and **DESIGN**.

### Step 4: Generate CR

After work is complete, **do not commit or push** — write the CR content, following the format defined in **CR**, to disk at **.cr.md**'s path (this must be a real file, not just text in your reply). Read the file back to confirm it was actually written before moving on. Then run `python .plato/scripts/write_status/cli.py coder wait <ticket-number> <task-id>`

### Step 5: Review via Q&A

Let the user review the generated code by asking you questions about it; answer each question they ask, fully and accurately, referring back to the actual code. Keep answering questions until the user is done and ready to reply with approve/reject/remake/etc.

### Step 6: Echo

Echo the content of **.cr.md** to the user, reproducing it **verbatim** in your reply — the CR itself is the report. Do not summarize, reword, or wrap it in your own format.

## CR Reply Handling

After **.cr.md** is created, wait for the user's reply and act as follows:

- **approve**:
  1. Check whether the user asked at least 3 questions about the generated code during **Step 5: Review via Q&A** in this session. If fewer than 3 questions were asked, **block**: tell the user they must ask at least 3 questions about the generated code before it can be approved, and stop here.
  2. For each `<rule file>: <rule text>` line in the **New Rules** section of **.cr.md**, append `<rule text>` to the **RULES** file `plato-workspace/role-rules/coder/<rule file>` (create the file if it does not exist)
  3. Run `python .plato/scripts/write_status/cli.py coder approve <ticket-number> <task-id>`
  4. Re-read **tasks.json**. If every task's `status` is now `DONE` (this was the last remaining task), tell the user: "Done. **Use `/exit` to leave this session**, then run `/plato <ticket-number>` to finish this ticket." and stop here — do not generate a next command.
  5. Otherwise:
     1. Run `python .plato/scripts/read_status/cli.py <ticket-number>`. It prints four lines: `role`, `task-id`, `status`, `session-id` — describing the next step.
     2. Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> <role> <status> <session-id> [task-id]` using those values (`task-id` only needed when `role` is `coder`). The script prints a single raw command line.
     3. Tell the user: "Done. **Use `/exit` to leave this session**, then run this to continue to the next task:\n\n    <command>\n\n(You can also get this command again at any time by running `/plato <ticket-number>`.)" — using the command from the previous step.

- **reject**:
  1. Revert all code changes from this session
  2. Run `python .plato/scripts/write_status/cli.py coder reject <ticket-number> <task-id>`
  3. Tell the user: "Change rejected. **Use `/exit` to leave this session**, then run `/plato <ticket-number>` to start this task over."

- **remake**: Using the full diff from `git diff HEAD`, regenerate **.cr.md** from scratch following the format in **CR**, overwrite it, echo it to the user verbatim (as in Step 6), and continue waiting for a reply. Do not modify **status.json**.

- **Any other reply (ask, modify, etc.)**: do not modify **.cr.md** or **status.json**

## Load External Files

Before starting the Startup Rules, read the following files:
- **CR** (`.plato/coder/COMMIT_REQUEST.md`)
- **RULES** (every `.md` file under `plato-workspace/role-rules/coder/`)
- **DESIGN** (`plato-workspace/tickets/<ticket-number>/DESIGN.md`), if it exists
- every `.md` file under `plato-workspace/project-context/`
