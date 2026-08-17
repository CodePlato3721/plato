from .common import load_plan_tasks, load_status, save_status, set_entry_status

ROLE = "planner"


def run(ticket_number: str, session_id: str) -> None:
    set_entry_status(ticket_number, ROLE, "IN_PROGRESS", session_id)


def wait(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "WAITING")


def approve(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "DONE")
    path, data = load_status(ticket_number)
    coder = data.setdefault("coder", {})
    existing = {task["id"]: task for task in coder.get("tasks", [])}
    coder["tasks"] = [
        existing.get(task["id"], {"id": task["id"], "status": "TODO"})
        for task in load_plan_tasks(ticket_number)
    ]
    save_status(path, data)


def reject(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "TODO", session_id="")
