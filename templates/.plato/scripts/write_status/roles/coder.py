import sys

from .common import delete_ticket_file, load_status, save_status


def _set_task_status(ticket_number: str, task_id: str, status: str, session_id: str | None = None) -> None:
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

    print(f"{task_id} not found in ticket {ticket_number} - the planner did not register this task", file=sys.stderr)
    sys.exit(1)


def run(ticket_number: str, task_id: str, session_id: str) -> None:
    _set_task_status(ticket_number, task_id, "IN_PROGRESS", session_id)


def wait(ticket_number: str, task_id: str) -> None:
    _set_task_status(ticket_number, task_id, "WAITING")


def approve(ticket_number: str, task_id: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    _set_task_status(ticket_number, task_id, "DONE")


def reject(ticket_number: str, task_id: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    _set_task_status(ticket_number, task_id, "TODO", session_id="")
