from .common import set_entry_status

ROLE = "planner"


def run(ticket_number: str, session_id: str) -> None:
    set_entry_status(ticket_number, ROLE, "IN_PROGRESS", session_id)


def wait(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "WAITING")


def approve(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "DONE")


def reject(ticket_number: str) -> None:
    set_entry_status(ticket_number, ROLE, "TODO", session_id="")
