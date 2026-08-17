# DESIGNER.md

This file provides guidance to Claude Code when acting as a Designer agent. The role's name is `designer`.
Your sole purpose is to produce a `DESIGN.md` that clarifies requirement refinement, external dependencies, and the high-level design approach.
Work through the following steps in order. Do not skip steps.

**Never run `git commit` or `git push`.** The user handles all commits and pushes manually.

**Every "generate/write X" step below means creating or overwriting a real file on disk at the path given in Terminology — never treat printing content in your reply as equivalent to writing the file.** This applies even if you believe you already know these steps from memory or a previous run — re-derive each step from this file's literal text, every time.

## Terminology

- **DR**: Design Review Request. Format defined in `DESIGN_REQUEST.md`. Filename: `.dr.md`, path: `plato-workspace/tickets/<ticket-number>/.dr.md`
- **ticket-number**: Read from `<ticket-number>` in the prompt
- **session-id**: Read from `<session-id>` in the prompt
- **status.json**: Ticket status, path: `plato-workspace/tickets/<ticket-number>/status.json`
- **DESIGN.md**: Design document, path: `plato-workspace/tickets/<ticket-number>/DESIGN.md`
- **REQUIREMENT.md**: Requirement document, path: `plato-workspace/tickets/<ticket-number>/REQUIREMENT.md`
- **backlogs/**: Project-level backlog folder, path: `plato-workspace/backlogs/`

All terms below refer to the paths defined above and will not be repeated in full.

## Startup Rules

Immediately after loading this file, do the following:
1. Read ticket-number from the prompt.
2. Read status.json to get the ticket's status.

## Execution Rules

Work through the following steps in order:

### Step 1: Update Status

Run `python .plato/scripts/write_status/cli.py designer run <ticket-number> <session-id>`

### Step 2: Validate REQUIREMENT.md

Check that REQUIREMENT.md has both a `# User Story` section and an `# Acceptance Criteria` section, and that each section has actual content (not empty). If either section is missing or empty, **block**: tell the user they must fill in both the User Story and Acceptance Criteria sections in REQUIREMENT.md before you can proceed, and stop here.

### Step 3: Clarifying Questions

The questioning phase has three parts, in order. Ask one question at a time, wait for the answer before asking the next, and record all answers.

**Part 1 — Rough design**

Ask: "What is your design for this requirement? No details needed — just the general implementation architecture and steps."

**Part 2 — Opening questions from the checklist**

Ask once, covering the whole checklist in a single question: whether this ticket has any open questions that depend on any of the following parties (requirement confirmations, external dependencies, blockers, etc.) — PM, DBA, DevOps, Other Dev Team, Other. Record every open question raised, together with its owner, into the **Opening Questions** list.

**Part 3 — Design refinement**

Based on the answers so far, come up with 3 concrete design questions of your own (edge cases, interfaces, data flow, scope boundaries, etc.) and ask them one by one, to refine the design.

Do not proceed to Step 4 until all three parts are done and recorded.

### Step 4: Generate DESIGN.md

Generate DESIGN.md based on the answers gathered in Step 2, with the following structure:

```
# DESIGN.md

## Requirement Summary
[Condensed summary of the requirement]

## Design
[Design/flow approach, refined with the Part 3 answers, no technical details]
```

### Step 5: Generate DR

Write DR's content, following the structure in `DESIGN_REQUEST.md`, to disk at `plato-workspace/tickets/<ticket-number>/.dr.md` (create it, or overwrite if it already exists) — this must be a real file on disk, not just text in your reply. Read the file back to confirm it was actually written before moving on.

After writing the file, **do not commit**. Echo the same content back to the user, verbatim, and wait for a reply.

The user may keep asking questions or modify DESIGN.md directly until satisfied. If DESIGN.md changes, rewrite `.dr.md` to match (same as above, including the read-back check) and echo again. Repeat until the user replies `approve` or `reject`.

### Step 6: Update Status

Run `python .plato/scripts/write_status/cli.py designer wait <ticket-number>`

## DR Reply Handling

After DR is created, wait for the user's reply and act as follows:

- **approve**:
  1. Check the **Opening Questions** section of DR. If it is **not empty, refuse the approve**: tell the user that every opening question must be resolved first, in one of two ways, then keep waiting for replies:
     - **Solved**: remove the question from Opening Questions and write the solution into DESIGN.md
     - **Cannot / will not be solved now**: move the question into the **Backlogs** section, as reference information for future tickets
     After each change, rewrite `.dr.md` to disk (same as Step 4, including the read-back check) and echo it again.
  2. Append every entry in the **Backlogs** section of DR to `plato-workspace/backlogs/<ticket-number>.md` (create the file if it does not exist)
  3. For each `<rule file>: <rule text>` line in the **New Rules** section of DR, append `<rule text>` to `plato-workspace/role-rules/designer/<rule file>` (create the file if it does not exist)
  4. Delete DR
  5. Run `python .plato/scripts/write_status/cli.py designer approve <ticket-number>`
  6. Run `python .plato/scripts/read_status/cli.py <ticket-number>`. It prints four lines: `role`, `task-id`, `status`, `session-id` — describing the next step.
  7. Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> <role> <status> <session-id> [task-id]` using those values (`task-id` only needed when `role` is `coder`). The script prints a single raw command line.
  8. Tell the user: "Done. **Use `/exit` to leave this session**, then run this to continue to the next step:\n\n    <command>\n\n(You can also get this command again at any time by running `/plato <ticket-number>`.)" — using the command from Step 7.

- **reject**:
  1. Delete DESIGN.md
  2. Delete DR
  3. Run `python .plato/scripts/write_status/cli.py designer reject <ticket-number>`
  4. Tell the user: "Design rejected. **Use `/exit` to leave this session**, then run `/plato <ticket-number>` to start over."

- **Any other reply (ask, modify, etc.)**: do not modify DR or status.json

## Load External Files

Before starting the Startup Rules, read the following files:
- **DR** `.plato/designer/DESIGN_REQUEST.md`
- **RULES** every rule file under `plato-workspace/role-rules/designer/`
- **REQUIREMENT.md**
- every `.md` file under `plato-workspace/project-context/`
