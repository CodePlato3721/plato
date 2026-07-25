# Defect Creation Flow

Reached when the ticket type (already determined by the entry point) is `defect`.

1. Ask the ticket title (free text): "What is the title of this ticket?"
2. Create `plato-workspace/tickets/<ticket-number>/` if it doesn't exist, and
   copy `templates/ticket/status.default.defect.json` into it as `status.json`.
3. Edit the new `status.json`:
   - set `type` to `defect`
   - set `title` to the given title
   - set `unit-test-path` to the `unit-test-path` value recorded in `plato-workspace/project-context/SETTINGS.md`
   - set `e2e-test-path` to the `e2e-test-path` value recorded in `plato-workspace/project-context/SETTINGS.md`
4. Run `python scripts/generate_command.py <ticket-number> fixer TODO ""` —
   the script will generate a new session-id automatically.
5. Create `plato-workspace/tickets/<ticket-number>/DEFECT.md` initialized with exactly these two empty sections:
   ```
   # Description

   # Steps to Reproduce

   ```
6. Tell the user:
   - The ticket workspace was created.
   - Show the script's output from step 4 as-is.
   - "Please fill in the defect report (what's broken, repro steps, expected vs actual) in `plato-workspace/tickets/<ticket-number>/DEFECT.md` before starting the fixer step."
