# Commit Lock

You've already seen `.dr.md`, `.tr.md`, and `.cr.md` (and `.fr.md` for
defects) show up several times by now. These are all **commit locks**.
Their purpose:

1. Summarize the current change, so a human can actually read and follow
   what happened.
2. Block the agent from committing code on its own. Once you `approve`,
   you can commit the code yourself, or ask Claude Code in the guide
   session to commit it for you.

## Why commit lock is needed

Agents love to commit code on their own and hand you back one giant PR that
nobody can realistically review. That's exactly what we're trying to
prevent. I wrote about the reasoning behind this design in [Code Review in
the Age of AI: From Review to
Audit](https://hackernoon.com/code-review-in-the-age-of-ai-from-review-to-audit)
— a commit lock stops the agent from committing on its own, and gives you a
guaranteed window to actually review the work.

## When a commit lock gets created

Once the agent in your working session finishes its work, it flips that
role's status in `status.json` to `WAITING` and, at the same time, writes
out its commit lock file.

## What happens after you reply

Once the commit lock is written, the agent asks for your reply — `approve`,
`reject`, and so on. What happens next depends on the role:

**reject**: the same for every role — it reverts whatever was done in this
session and moves the role's status from `WAITING` back to `TODO`. So this
one isn't repeated separately under each role below.

### designer

**approve**: moves everything in **Backlogs** to
`plato-workspace/backlogs/<ticket-number>.md`, and moves everything in
**New Rules** into `plato-workspace/role-rules/designer/<file>`.

### planner

*(complex feature tickets only.)*

**approve**: moves everything in **New Rules** into
`plato-workspace/role-rules/planner/<file>`. (`.tr.md` has no Backlogs
section, so there's nothing to move there.)

### coder

**approve**: moves everything in **New Rules** into
`plato-workspace/role-rules/coder/<file>`.

**remake**: after a few rounds of back-and-forth with the agent that
changed the code, use `remake` to regenerate `.cr.md` from scratch so it
matches the current diff.

### fixer

**approve**: moves everything in **New Rules** into
`plato-workspace/role-rules/fixer/<file>`.

**remake**: same idea as coder's — after further back-and-forth changes the
code, `remake` regenerates `.fr.md` from scratch.

---

Once these actions are done, the agent deletes the commit lock file and
marks that role's status in `status.json` as `DONE`, then tells you to
`/exit` the session and commit the code yourself. Only at that point is
this agent's work actually finished.

---

**Previous:** [← 03. Feature](03-feature.md) · **Next:** [05. ABR →](05-abr.md)
