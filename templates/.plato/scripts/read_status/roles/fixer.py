from .common import find_role_step

ROLE = "fixer"


def find(status: dict) -> dict | None:
    return find_role_step(status, ROLE)
