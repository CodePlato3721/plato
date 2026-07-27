# defect

defect is the second ticket type Plato supports. It's a lot simpler than
feature — a defect ticket has exactly one role: **fixer**.

# fixer

When Plato initializes a defect ticket, it generates an empty `DEFECT.md`.
Before fixer starts working, it checks that file for a `# Description`
section and a `# Steps to Reproduce` section, and that neither is empty.

> **📌 Note:** fixer is also a foreground agent, same as designer.

fixer first tries to reproduce the defect. Once it reproduces successfully,
it starts analyzing the root cause.

Once it has a root cause, you and fixer confirm together whether it's
correct. Then you decide what kind of defect this actually is:

- **False positive**: not a real bug — just delete this defect.
- **Missing requirement**: what's "broken" is actually a feature that was
  never built — delete this defect and open a new feature ticket instead.
- **Data issue**: effectively a false positive — delete this defect.
- **Real defect**: move on to the next step.

If it's confirmed as a real defect, let the agent go ahead and implement
the solution.

Once the fix is implemented, the agent generates `.fr.md` and waits for
your reply. You must ask it at least three questions before you're allowed
to reply `approve`.

Once `.fr.md` is approved, fixer:

1. Sets fixer's status in `status.json` to `DONE`.
2. Files New Rules into `plato-workspace/role-rules/fixer/<file>`.
3. Deletes `.fr.md`.
4. Tells you to `/exit` the agent and commit the code yourself.

---

**Previous:** [← 05. ABR](05-abr.md)
