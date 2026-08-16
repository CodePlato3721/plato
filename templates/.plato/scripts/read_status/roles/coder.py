from .common import load_plan_tasks, result

ROLE = "coder"


def find(status: dict, ticket_number: str) -> dict | None:
    coder = status.get(ROLE, {})
    tasks = coder.get("tasks", [])

    active_task = next((t for t in tasks if t.get("status") != "DONE"), None)
    if active_task is None:
        known_ids = {t.get("id") for t in tasks}
        active_task = next((pt for pt in load_plan_tasks(ticket_number) if pt.get("id") not in known_ids), None)

    if active_task is not None:
        return result(
            ROLE,
            active_task.get("status", "TODO"),
            active_task.get("coder", {}).get("session-id", ""),
            task_id=active_task.get("id", ""),
        )

    if load_plan_tasks(ticket_number):
        # Every task in tasks.json is registered in coder.tasks and DONE.
        return None

    # tasks.json doesn't exist yet or is empty — nothing for the coder to do yet.
    return result(ROLE, coder.get("status", "TODO"), "")
