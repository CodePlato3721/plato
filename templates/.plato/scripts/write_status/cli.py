import sys

from roles import ROLE_MODULES, coder
from roles.common import load_status

USAGE = """usage:
  cli.py <designer|planner|fixer> run <ticket-number> <session-id>
  cli.py <designer|planner|fixer> <wait|approve|reject> <ticket-number>
  cli.py coder run <ticket-number> <task-id> <session-id>            (complex_feature)
  cli.py coder <wait|approve|reject> <ticket-number> <task-id>       (complex_feature)
  cli.py coder run <ticket-number> <session-id>                     (simple_feature)
  cli.py coder <wait|approve|reject> <ticket-number>                (simple_feature)"""


def bad_usage() -> None:
    print(USAGE, file=sys.stderr)
    sys.exit(1)


def main() -> None:
    args = sys.argv[1:]
    if len(args) < 2:
        bad_usage()

    command, sub_command, *rest = args
    if sub_command not in ("run", "wait", "approve", "reject"):
        bad_usage()

    if command in ROLE_MODULES:
        module = ROLE_MODULES[command]
        expected = 2 if sub_command == "run" else 1
        if len(rest) != expected:
            bad_usage()
        getattr(module, sub_command)(*rest)
        return

    if command != "coder":
        bad_usage()
        return

    # coder's shape (single entry vs task list) depends on this ticket's status.json
    # `type` field — never inferred from argument count.
    if not rest:
        bad_usage()
    _, data = load_status(rest[0])
    is_simple = data.get("type") == "simple_feature"

    if is_simple:
        expected = 2 if sub_command == "run" else 1
        fn_name = f"{sub_command}_simple"
    else:
        expected = 3 if sub_command == "run" else 2
        fn_name = sub_command

    if len(rest) != expected:
        bad_usage()

    getattr(coder, fn_name)(*rest)


if __name__ == "__main__":
    main()
