import sys

from roles import ROLE_STRATEGIES
from roles.session import prepare_session_id


def main() -> None:
    if len(sys.argv) not in (5, 6):
        print(
            "usage: cli.py <ticket-number> <role> <status> <session-id> [task-id]",
            file=sys.stderr,
        )
        sys.exit(1)

    ticket_number, role, status, session_id = sys.argv[1:5]
    task_id = sys.argv[5] if len(sys.argv) == 6 else ""

    strategy = ROLE_STRATEGIES.get(role)
    if not strategy:
        print(f"unknown role: {role}", file=sys.stderr)
        sys.exit(1)

    try:
        session_id = prepare_session_id(session_id)
        print(strategy.get_command(status, session_id, ticket_number, task_id))
    except ValueError as e:
        print(e, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
