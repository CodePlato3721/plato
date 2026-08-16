import sys

from roles import ROLE_MODULES, coder

USAGE = """usage:
  cli.py <designer|planner|fixer> run <ticket-number> <session-id>
  cli.py <designer|planner|fixer> <wait|approve|reject> <ticket-number>
  cli.py coder run <ticket-number> <task-id> <session-id>
  cli.py coder <wait|approve|reject> <ticket-number> <task-id>"""


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
    elif command == "coder":
        module = coder
        expected = 3 if sub_command == "run" else 2
    else:
        bad_usage()
        return

    if len(rest) != expected:
        bad_usage()

    getattr(module, sub_command)(*rest)


if __name__ == "__main__":
    main()
