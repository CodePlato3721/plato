# Complex Feature Continue Flow

Reached when `status.json`'s `type` field is `complex_feature`.

## Step 1 — Report current status

Run `python scripts/status_report.py <ticket-number>` and show
its output to the user as-is. It reads
`plato-workspace/tickets/<ticket-number>/status.json` and formats it as:

```
ticket number: <ticket number>
title: <title>
designer: <role status>
planner: <role status>
coder: <role status>
tasks:
<task id1>: <role status>
<task id2>: <role status>
...
```

(`tasks` comes from `coder.tasks[]`; if the list is empty it prints
`tasks: (none yet)`.)

## Step 2 — Find the active task

Run `python .plato/scripts/read_status/cli.py <ticket-number>`.
It prints four lines:

```
role: <designer|planner|coder|none>
task-id: <task id, only set when role is coder>
status: <TODO|IN_PROGRESS|WAITING|DONE>
session-id: <value, or empty>
```

If `role` is `none`, the ticket is fully complete — tell the user that and stop, no command to generate.

## Step 3 — Generate the command

Run `python .plato/scripts/gen_cmd/cli.py <ticket-number> <role> <status> <session-id> [task-id]`
using the four values Step 2 reported (`task-id` only needed when `role` is
`coder`). The script prints a single raw command line. Wrap it with the
appropriate message before showing it to the user:

- **`TODO`**: "You can start this step now:\n\n    <command>"
- **`IN_PROGRESS`**: "The `<role>` agent is currently running. Please wait — once it finishes you can resume the session with:\n\n    <command>"
- **`WAITING`**: "The `<role>` agent finished its run and is waiting for your input. Resume the session with:\n\n    <command>"

If `status` is `TODO` and `session-id` was empty, the script generates a new
UUID and uses it in the printed command. The session-id is NOT written into
`status.json` at this point — the role agent writes it in its own Step 1
when it starts. The user may also replace the session-id in the command with
their own before running it. Never generate or fabricate a `session-id`
yourself — the script is the only place that does that.
