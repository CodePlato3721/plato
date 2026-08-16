import sys

from roles import coder, designer, fixer, planner
from roles.common import read_status, result, status_path


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: cli.py <ticket-number>", file=sys.stderr)
        sys.exit(1)

    ticket_number = sys.argv[1]
    if not status_path(ticket_number).exists():
        print(f"status.json not found for ticket {ticket_number}", file=sys.stderr)
        sys.exit(1)

    status = read_status(ticket_number)

    if status.get("type") == "defect":
        step = fixer.find(status)
    else:
        step = designer.find(status) or planner.find(status) or coder.find(status, ticket_number)
    step = step or result("none", "DONE", "")

    print(f"role: {step['role']}")
    print(f"task-id: {step['task_id']}")
    print(f"status: {step['status']}")
    print(f"session-id: {step['session_id']}")


if __name__ == "__main__":
    main()
