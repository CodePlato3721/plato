from .common import find_role_step

ROLE = "planner"


def find(status: dict) -> dict | None:
    return find_role_step(status, ROLE)
