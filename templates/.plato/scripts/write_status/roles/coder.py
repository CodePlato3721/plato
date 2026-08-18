import sys

from .common import delete_ticket_file, load_status, save_status, set_entry_status

ROLE = "coder"


def _set_task_status(ticket_number: str, task_id: str, status: str, session_id: str | None = None) -> None:
    path, data = load_status(ticket_number)
    tasks = data.get(ROLE, {}).get("tasks", [])

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


# simple_feature: coder is a single role entry, same shape as designer/fixer — no task-id.


def run_simple(ticket_number: str, session_id: str) -> None:
    set_entry_status(ticket_number, ROLE, "IN_PROGRESS", session_id)


def wait_simple(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "WAITING")


def approve_simple(ticket_number: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    set_entry_status(ticket_number, ROLE, "DONE")


def reject_simple(ticket_number: str) -> None:
    delete_ticket_file(ticket_number, ".cr.md")
    set_entry_status(ticket_number, ROLE, "TODO", session_id="")
