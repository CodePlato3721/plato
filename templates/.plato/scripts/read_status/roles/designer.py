from .common import find_role_step

ROLE = "designer"


def find(status: dict) -> dict | None:
    return find_role_step(status, ROLE)
