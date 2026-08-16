import json
from pathlib import Path


def status_path(ticket_number: str) -> Path:
    return Path("plato-workspace/tickets") / ticket_number / "status.json"


def read_status(ticket_number: str) -> dict:
    return json.loads(status_path(ticket_number).read_text(encoding="utf-8"))


def load_plan_tasks(ticket_number: str) -> list:
    tasks_path = Path("plato-workspace/tickets") / ticket_number / "tasks.json"
    if not tasks_path.exists():
        return []
    return json.loads(tasks_path.read_text(encoding="utf-8")).get("tasks", [])


def result(role: str, status: str, session_id: str, task_id: str = "") -> dict:
    return {"role": role, "status": status, "session_id": session_id, "task_id": task_id}


def find_role_step(status: dict, role: str) -> dict | None:
    entry = status.get(role, {})
    if entry.get("status") == "DONE":
        return None
    return result(role, entry.get("status", "TODO"), entry.get("session-id", ""))
