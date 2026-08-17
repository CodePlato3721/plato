# Defect Continue Flow

Reached when `status.json`'s `type` field is `defect`.

## Step 1 — Report current status

Run `python scripts/status_report.py <ticket-number>` and show
its output to the user as-is. It reads
`plato-workspace/tickets/<ticket-number>/status.json` and formats it as:

```
ticket number: <ticket number>
title: <title>
fixer: <role status>
```

## Step 2 — Find the active step

Run `python .plato/scripts/read_status/cli.py <ticket-number>`.
It prints four lines:

```
role: <fixer|none>
task-id: (always empty for defect tickets)
status: <TODO|IN_PROGRESS|WAITING|DONE>
session-id: <value, or empty>
```

If `role` is `none`, the ticket is fully complete — tell the user that and stop, no command to generate.

## Step 3 — Generate the command

Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> fixer <status> <session-id>`
using the values Step 2 reported. The script prints a single raw command line. Wrap it with the
appropriate message before showing it to the user:

- **`TODO`**: "You can start this step now:\n\n    <command>"
- **`IN_PROGRESS`**: "The `fixer` agent is currently running. Please wait — once it finishes you can resume the session with:\n\n    <command>"
- **`WAITING`**: "The `fixer` agent finished its run and is waiting for your input. Resume the session with:\n\n    <command>"

If `status` is `TODO` and `session-id` was empty, the script generates a new
UUID and uses it in the printed command. The session-id is NOT written into
`status.json` at this point — the fixer agent writes it in its own Step 1
when it starts. The user may also replace the session-id in the command with
their own before running it. Never generate or fabricate a `session-id`
yourself — the script is the only place that does that.
