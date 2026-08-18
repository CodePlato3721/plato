from .common import find_role_step, result

ROLE = "coder"


def find_simple(status: dict) -> dict | None:
    """simple_feature: coder is a single role entry, same shape as designer/fixer."""
    return find_role_step(status, ROLE)


def find(status: dict) -> dict | None:
    coder = status.get(ROLE, {})
    tasks = coder.get("tasks", [])

    active_task = next((t for t in tasks if t.get("status") != "DONE"), None)
    if active_task is not None:
        return result(
            ROLE,
            active_task.get("status", "TODO"),
            active_task.get("coder", {}).get("session-id", ""),
            task_id=active_task.get("id", ""),
        )

    if tasks:
        # Every task the planner registered is DONE.
        return None

    # The planner hasn't registered any tasks yet — nothing for the coder to do.
    return result(ROLE, coder.get("status", "TODO"), "")
