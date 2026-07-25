import sys

from tasks.task_finder import ActiveStepFinder


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: find_active_step.py <ticket-number>", file=sys.stderr)
        sys.exit(1)

    finder = ActiveStepFinder(sys.argv[1])
    if not finder.exists():
        print(f"status.json not found for ticket {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    result = finder.find()
    print(f"role: {result['role']}")
    print(f"task-id: {result['task_id']}")
    print(f"status: {result['status']}")
    print(f"session-id: {result['session_id']}")


if __name__ == "__main__":
    main()
