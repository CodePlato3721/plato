# Finish Flow

Reached when a ticket's work is fully complete — `defect`: `fixer.status` is
`DONE`; `feature`: `coder.tasks` is non-empty and every task's `status` is
`DONE`. Shared by both feature and defect tickets.

## Step 1 — Ask about the ticket folder

Tell the user all work on this ticket is now complete. Ask, using
`AskUserQuestion`, whether to keep
`plato-workspace/tickets/<ticket-number>/`:

- Keep it (recommended)
- Delete it

If the user chooses to delete it, delete
`plato-workspace/tickets/<ticket-number>/` and everything under it.

## Step 2 — Offer to commit & push

Regardless of the Step 1 choice, ask the user whether to commit and push the
current changes.

- If the user agrees, stage all changes, commit with a message summarizing
  the ticket's work, and push.
- Otherwise, stop here without committing or pushing.
