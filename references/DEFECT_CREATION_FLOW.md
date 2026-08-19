# Defect Creation Flow

Reached when the ticket type (already determined by the entry point) is `defect`.

1. Ask the ticket title (free text): "What is the title of this ticket?"
2. Create and switch to a new git branch named `defect/<ticket-number>`.
3. Create `plato-workspace/tickets/<ticket-number>/` if it doesn't exist, and
   copy `templates/ticket/status.default.defect.json` into it as `status.json`.
4. Edit the new `status.json`: set `title` to the given title.
5. Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> fixer TODO ""` —
   the script will generate a new session-id automatically.
6. Create `plato-workspace/tickets/<ticket-number>/DEFECT.md` initialized with exactly these two empty sections:
   ```
   # Description

   # Steps to Reproduce

   ```
7. Tell the user:
   - The ticket workspace was created.
   - Show the script's output from step 5 as-is.
   - "Please fill in the defect report (what's broken, repro steps, expected vs actual) in `plato-workspace/tickets/<ticket-number>/DEFECT.md` before starting the fixer step."
