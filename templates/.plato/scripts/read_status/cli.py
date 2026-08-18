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
    ticket_type = status.get("type")

    if ticket_type == "defect":
        step = fixer.find(status)
    elif ticket_type == "simple_feature":
        step = designer.find(status) or coder.find_simple(status)
    else:
        # complex_feature
        step = designer.find(status) or planner.find(status) or coder.find(status)
    step = step or result("none", "DONE", "")

    print(f"role: {step['role']}")
    print(f"task-id: {step['task_id']}")
    print(f"status: {step['status']}")
    print(f"session-id: {step['session_id']}")


if __name__ == "__main__":
    main()
