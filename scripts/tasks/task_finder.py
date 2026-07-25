import json
from pathlib import Path


def _load_plan_tasks(ticket_number: str) -> list:
    tasks_path = Path("plato-workspace/tickets") / ticket_number / "tasks.json"
    if not tasks_path.exists():
        return []
    return json.loads(tasks_path.read_text(encoding="utf-8")).get("tasks", [])


def _find_active_coder_task(coder: dict, ticket_number: str) -> dict | None:
    tasks = coder.get("tasks", [])

    active_task = next((t for t in tasks if t.get("status") != "DONE"), None)
    if active_task is not None:
        return active_task

    known_ids = {t.get("id") for t in tasks}
    return next((pt for pt in _load_plan_tasks(ticket_number) if pt.get("id") not in known_ids), None)


class ActiveStepFinder:
    def __init__(self, ticket_number: str):
        self.ticket_number = ticket_number
        self._status_path = Path("plato-workspace/tickets") / ticket_number / "status.json"

    def exists(self) -> bool:
        return self._status_path.exists()

    def find(self) -> dict:
        status = json.loads(self._status_path.read_text(encoding="utf-8"))

        if status.get("type") == "defect":
            fixer = status.get("fixer", {})
            if fixer.get("status") != "DONE":
                return self._result("fixer", fixer.get("status", "TODO"), fixer.get("session-id", ""))
            return self._result("none", "DONE", "")

        designer = status.get("designer", {})
        if designer.get("status") != "DONE":
            return self._result("designer", designer.get("status", "TODO"), designer.get("session-id", ""))

        planner = status.get("planner", {})
        if planner.get("status") != "DONE":
            return self._result("planner", planner.get("status", "TODO"), planner.get("session-id", ""))

        coder = status.get("coder", {})
        active_task = _find_active_coder_task(coder, self.ticket_number)
        if active_task is not None:
            return self._result(
                "coder",
                active_task.get("status", "TODO"),
                active_task.get("coder", {}).get("session-id", ""),
                task_id=active_task.get("id", ""),
            )

        if _load_plan_tasks(self.ticket_number):
            # Every task in tasks.json is registered in coder.tasks and DONE.
            # (coder.status itself is never written by any role step — it's
            # not a reliable completion signal — so completion is derived
            # from tasks.json coverage instead.)
            return self._result("none", "DONE", "")

        # tasks.json doesn't exist yet or is empty — nothing for the coder
        # to do yet.
        return self._result("coder", coder.get("status", "TODO"), "")

    @staticmethod
    def _result(role: str, status: str, session_id: str, task_id: str = "") -> dict:
        return {"role": role, "status": status, "session_id": session_id, "task_id": task_id}
