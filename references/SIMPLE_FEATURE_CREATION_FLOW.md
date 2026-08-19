# Simple Feature Creation Flow

Reached when the ticket type (already determined by the entry point) is `simple_feature`.

1. Ask the ticket title (free text): "What is the title of this ticket?"
2. Create and switch to a new git branch named `feature/<ticket-number>`.
3. Create `plato-workspace/tickets/<ticket-number>/` if it doesn't exist, and
   copy `templates/ticket/status.default.simple_feature.json` into it as `status.json`.
4. Edit the new `status.json`: set `title` to the given title.
5. Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> designer TODO ""` —
   the script will generate a new session-id automatically.
6. Create `plato-workspace/tickets/<ticket-number>/REQUIREMENT.md` initialized with exactly these two empty sections:
   ```
   # User Story

   # Acceptance Criteria

   ```
7. Tell the user:
   - The ticket workspace was created.
   - Show the script's output from step 5 as-is.
   - "Please fill in your requirements in `plato-workspace/tickets/<ticket-number>/REQUIREMENT.md` before starting the designer step."
