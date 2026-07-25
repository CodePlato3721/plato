import sys

from status.ticket_status import TicketStatus

sys.stdout.reconfigure(encoding="utf-8")


def format_report(data: dict) -> str:
    lines = [
        f"ticket number: {data['ticket_number']}",
        f"title: {data['title']}",
    ]

    if data.get("type") == "defect":
        lines.append(f"fixer: {data['fixer']}")
        return "\n".join(lines)

    lines += [
        f"designer: {data['designer']}",
        f"planner: {data['planner']}",
        f"coder: {data['coder']}",
        "tasks:",
    ]
    if data["tasks"]:
        for task in data["tasks"]:
            lines.append(f"{task['id']}: {task['status']}")
    else:
        lines.append("(none yet)")
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) != 2:
        print("usage: status_report.py <ticket-number>", file=sys.stderr)
        sys.exit(1)

    ticket = TicketStatus(sys.argv[1])
    if not ticket.exists():
        print(f"status.json not found for ticket {sys.argv[1]}", file=sys.stderr)
        sys.exit(1)

    print(format_report(ticket.read()))


if __name__ == "__main__":
    main()
