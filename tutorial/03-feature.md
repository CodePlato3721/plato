# feature

A feature ticket is either **simple** or **complex** — you choose which
when you create the ticket. Both start the same way, with **designer**,
then diverge:

- **simple**: designer → **coder**, no planning phase. Coder implements the
  whole feature in a single session.
- **complex**: designer → **planner** → **coder**. planner splits the work
  into `tasks.json`, and coder implements it one task at a time — every
  task gets a brand-new coder session, run strictly one after another.

Roughly:

- **designer** reads `REQUIREMENT.md` and produces `DESIGN.md`.
- **planner** *(complex only)* reads `DESIGN.md` and produces `tasks.json`.
- **coder** implements the work — for **complex**, one task from
  `tasks.json` at a time; for **simple**, the whole feature in one pass.

`status.json` is what tracks the ticket's progress through all of this. You
can open it directly at any time to see exactly where the ticket stands.

# roles

## designer

designer reads your requirement from `REQUIREMENT.md`. That file must have
two sections filled in: **User Story** and **Acceptance Criteria**.

designer then walks a checklist and asks you, one item at a time, whether
this ticket has any open questions against it. These get collected as
**Opening Questions**. Once that's done, it writes a `.dr.md` file — this
is both a summary of the design and a commit-lock, so the agent can't just
run off and commit code on its own.

You must clear every Opening Question before you can move on. A question
you can't or don't want to resolve now isn't blocking forever — you can
delete it, or move it into the **Backlogs** section instead.

If, while working with the agent, you think of a rule worth keeping around,
add it to the **New Rules** section. New Rules is a list, one entry per
line, in the form `<file>: <rule>`.

Once you and the agent have refined `DESIGN.md` together and every Opening
Question is cleared, reply `approve` to move on. Once you do, designer
will:

1. Move everything in **Backlogs** to
   `plato-workspace/backlogs/<ticket-number>.md`.
2. Move everything in **New Rules** to
   `plato-workspace/role-rules/designer/<file>`.
3. Delete `.dr.md`.
4. Tell you to `/exit` the agent and commit the code yourself.

If you're unhappy with the result, reply `reject` instead — this discards
the current work and lets you start the step over from scratch.

## planner

*(complex feature tickets only — simple feature tickets skip straight from
designer to coder, no planning phase.)*

Once designer has produced `DESIGN.md`, ask the guide session with `/plato
<ticket-number>`. It gives you the next command to run — something like
`claude --session-id ...`.

Take that command to the working session and run it there. This starts a
planner session, interactively, same as designer. It lists the
task-splitting strategies under `.plato/planner/strategies/`, recommends
one based on `DESIGN.md`, and asks you to pick one before it splits the
design into tasks.

If you ever exit the session before planner has produced `tasks.json` and
a `.tr.md` file, ask the guide session again with `/plato <ticket-number>`,
and it gives you a resume command this time — something like `claude
--resume ...`.

Once planner is awake, you must ask it at least three questions about
`tasks.json` to review the split — you can't `approve` without doing this.

If you're happy with `tasks.json`, reply `approve`. Once you do, planner
will:

1. Move everything in **New Rules** to
   `plato-workspace/role-rules/planner/<file>`.
2. Delete `.tr.md`.
3. Tell you to `/exit` the agent and commit the code yourself.

## coder

**Complex feature:** once planning is done, ask the guide session again:
`/plato <ticket-number>`. It gives you the command for the **first** task.
Take it to the working session and run it there — coder implements the
task interactively and produces a `.cr.md` file when it's done.

**Simple feature:** once designer is done, ask the guide session: `/plato
<ticket-number>`. It gives you the command for coder directly — there's no
planner step in between. Coder implements the whole feature in this one
session and produces a `.cr.md` file when it's done.

If you exit before it's done, ask the guide session again — `/plato
<ticket-number>` — and it gives you the command to resume coder.

Once coder is awake, you must also ask it at least three questions about
the code to review it before you're allowed to reply `approve`.

> **Suggestion:** ask at least ten questions, and refactor the code as you
> review it. Refactoring becomes a way of actually understanding — and
> reviewing — the code, not just a cleanup step.

If the code needs significant changes, reply `remake` — coder regenerates
`.cr.md` from scratch. If the code looks good, reply `approve`. Once you
do, coder will:

1. Move everything in **New Rules** to
   `plato-workspace/role-rules/coder/<file>`.
2. Delete `.cr.md`.
3. Tell you to `/exit` the agent and commit the code yourself.

**Complex feature:** repeat this whole cycle — run task, question, approve
— for every task in `tasks.json`, until all of them are done.

**Simple feature:** approving is the last step — the ticket is done as
soon as this single `.cr.md` is approved.

---

**Previous:** [← 02. Prepare workspace](02-prepare.md) · **Next:** [04. Commit Lock →](04-commit-lock.md)
