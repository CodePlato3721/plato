import argparse
import json
import sys
from pathlib import Path


def status_path(ticket_number: str) -> Path:
    return Path("plato-workspace/tickets") / ticket_number / "status.json"


def load_status(ticket_number: str) -> tuple[Path, dict]:
    path = status_path(ticket_number)
    if not path.exists():
        print(f"status.json not found for ticket {ticket_number}", file=sys.stderr)
        sys.exit(1)
    return path, json.loads(path.read_text(encoding="utf-8"))


def save_status(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


ROLES = ("designer", "planner")


def set_role_status(ticket_number: str, role: str, status: str, session_id: str | None = None) -> None:
    if role not in ROLES:
        print(f"unknown role {role} - expected one of {', '.join(ROLES)}", file=sys.stderr)
        sys.exit(1)

    path, data = load_status(ticket_number)
    entry = data.setdefault(role, {})
    entry["status"] = status
    if session_id is not None:
        entry["session-id"] = session_id
    save_status(path, data)
    print(f"{role} in ticket {ticket_number} set to {status}")


def role_run(ticket_number: str, role: str, session_id: str) -> None:
    set_role_status(ticket_number, role, "IN_PROGRESS", session_id)


def role_wait(ticket_number: str, role: str) -> None:
    set_role_status(ticket_number, role, "WAITING")


def role_approve(ticket_number: str, role: str) -> None:
    set_role_status(ticket_number, role, "DONE")


def role_reject(ticket_number: str, role: str) -> None:
    set_role_status(ticket_number, role, "TODO", session_id="")


def set_task_status(ticket_number: str, task_id: str, status: str, session_id: str | None = None) -> None:
    path, data = load_status(ticket_number)
    tasks = data.get("coder", {}).get("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = status
            if session_id is not None:
                task.setdefault("coder", {})["session-id"] = session_id
            save_status(path, data)
            print(f"{task_id} in ticket {ticket_number} set to {status}")
            return

    print(f"{task_id} not found in ticket {ticket_number} - run it first", file=sys.stderr)
    sys.exit(1)


def task_run(ticket_number: str, task_id: str, session_id: str) -> None:
    path, data = load_status(ticket_number)
    tasks = data.setdefault("coder", {}).setdefault("tasks", [])

    for task in tasks:
        if task.get("id") == task_id:
            task["status"] = "IN_PROGRESS"
            task.setdefault("coder", {})["session-id"] = session_id
            save_status(path, data)
            print(f"{task_id} in ticket {ticket_number} set to IN_PROGRESS")
            return

    tasks.append({"id": task_id, "status": "IN_PROGRESS", "coder": {"session-id": session_id}})
    save_status(path, data)
    print(f"registered {task_id} in ticket {ticket_number} and set to IN_PROGRESS")


def task_wait(ticket_number: str, task_id: str) -> None:
    set_task_status(ticket_number, task_id, "WAITING")


def delete_ticket_file(ticket_number: str, filename: str) -> None:
    path = Path("plato-workspace/tickets") / ticket_number / filename
    if path.exists():
        path.unlink()
        print(f"deleted {path.as_posix()}")


def task_approve(ticket_number: str, task_id: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    set_task_status(ticket_number, task_id, "DONE")


def task_reject(ticket_number: str, task_id: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    set_task_status(ticket_number, task_id, "TODO", session_id="")


def set_fixer_status(ticket_number: str, status: str, session_id: str | None = None) -> None:
    path, data = load_status(ticket_number)
    entry = data.setdefault("fixer", {})
    entry["status"] = status
    if session_id is not None:
        entry["session-id"] = session_id
    save_status(path, data)
    print(f"fixer in ticket {ticket_number} set to {status}")


def fixer_run(ticket_number: str, session_id: str) -> None:
    set_fixer_status(ticket_number, "IN_PROGRESS", session_id)


def fixer_wait(ticket_number: str) -> None:
    set_fixer_status(ticket_number, "WAITING")


def fixer_approve(ticket_number: str) -> None:
    delete_ticket_file(ticket_number, ".fr.md")
    set_fixer_status(ticket_number, "DONE")


def fixer_reject(ticket_number: str) -> None:
    delete_ticket_file(ticket_number, ".fr.md")
    set_fixer_status(ticket_number, "TODO", session_id="")


def main() -> None:
    parser = argparse.ArgumentParser(prog="status_cli.py", description="Manage status.json for a ticket")
    subparsers = parser.add_subparsers(dest="command", required=True)

    for role in ROLES:
        role_parser = subparsers.add_parser(role, help=f"{role} role status commands")
        role_subparsers = role_parser.add_subparsers(dest="role_command", required=True)

        role_run_parser = role_subparsers.add_parser(
            "run", help=f"set {role}'s status to IN_PROGRESS and record its session-id"
        )
        role_run_parser.add_argument("ticket_number")
        role_run_parser.add_argument("session_id")

        role_wait_parser = role_subparsers.add_parser("wait", help=f"set {role}'s status to WAITING")
        role_wait_parser.add_argument("ticket_number")

        role_approve_parser = role_subparsers.add_parser("approve", help=f"set {role}'s status to DONE")
        role_approve_parser.add_argument("ticket_number")

        role_reject_parser = role_subparsers.add_parser(
            "reject", help=f"set {role}'s status back to TODO and clear its session-id"
        )
        role_reject_parser.add_argument("ticket_number")

    coder_parser = subparsers.add_parser("coder", help="coder task status commands")
    coder_subparsers = coder_parser.add_subparsers(dest="coder_command", required=True)

    run_parser = coder_subparsers.add_parser(
        "run", help="set a task's status to IN_PROGRESS and record its session-id, registering the task if needed"
    )
    run_parser.add_argument("ticket_number")
    run_parser.add_argument("task_id")
    run_parser.add_argument("session_id")

    wait_parser = coder_subparsers.add_parser("wait", help="set a task's status to WAITING")
    wait_parser.add_argument("ticket_number")
    wait_parser.add_argument("task_id")

    approve_parser = coder_subparsers.add_parser("approve", help="delete .cr.md and set a task's status to DONE")
    approve_parser.add_argument("ticket_number")
    approve_parser.add_argument("task_id")

    reject_parser = coder_subparsers.add_parser(
        "reject", help="delete .cr.md, set a task's status back to TODO and clear its session-id"
    )
    reject_parser.add_argument("ticket_number")
    reject_parser.add_argument("task_id")

    fixer_parser = subparsers.add_parser("fixer", help="fixer role status commands (defect tickets)")
    fixer_subparsers = fixer_parser.add_subparsers(dest="fixer_command", required=True)

    fixer_run_parser = fixer_subparsers.add_parser(
        "run", help="set fixer's status to IN_PROGRESS and record its session-id"
    )
    fixer_run_parser.add_argument("ticket_number")
    fixer_run_parser.add_argument("session_id")

    fixer_wait_parser = fixer_subparsers.add_parser("wait", help="set fixer's status to WAITING")
    fixer_wait_parser.add_argument("ticket_number")

    fixer_approve_parser = fixer_subparsers.add_parser(
        "approve", help="delete .fr.md and set fixer's status to DONE"
    )
    fixer_approve_parser.add_argument("ticket_number")

    fixer_reject_parser = fixer_subparsers.add_parser(
        "reject", help="delete .fr.md, set fixer's status back to TODO and clear its session-id"
    )
    fixer_reject_parser.add_argument("ticket_number")

    args = parser.parse_args()

    if args.command in ROLES and args.role_command == "run":
        role_run(args.ticket_number, args.command, args.session_id)
    elif args.command in ROLES and args.role_command == "wait":
        role_wait(args.ticket_number, args.command)
    elif args.command in ROLES and args.role_command == "approve":
        role_approve(args.ticket_number, args.command)
    elif args.command in ROLES and args.role_command == "reject":
        role_reject(args.ticket_number, args.command)
    elif args.command == "coder" and args.coder_command == "run":
        task_run(args.ticket_number, args.task_id, args.session_id)
    elif args.command == "coder" and args.coder_command == "wait":
        task_wait(args.ticket_number, args.task_id)
    elif args.command == "coder" and args.coder_command == "approve":
        task_approve(args.ticket_number, args.task_id)
    elif args.command == "coder" and args.coder_command == "reject":
        task_reject(args.ticket_number, args.task_id)
    elif args.command == "fixer" and args.fixer_command == "run":
        fixer_run(args.ticket_number, args.session_id)
    elif args.command == "fixer" and args.fixer_command == "wait":
        fixer_wait(args.ticket_number)
    elif args.command == "fixer" and args.fixer_command == "approve":
        fixer_approve(args.ticket_number)
    elif args.command == "fixer" and args.fixer_command == "reject":
        fixer_reject(args.ticket_number)


if __name__ == "__main__":
    main()
