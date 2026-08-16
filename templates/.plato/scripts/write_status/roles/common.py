import json
import sys
from pathlib import Path


def status_path(ticket_number: str) -> Path:
    return Path("plato-workspace/tickets") / ticket_number / "status.json"


def load_status(ticket_number: str) -> tuple[Path, dict]:
    path = status_path(ticket_number)
    if not path.exists():
        print(f"status.json not found for ticket {ticket_number}", file=sys.stderr)
        sys.exit(1)
    return path, json.loads(path.read_text(encoding="utf-8"))


def save_status(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, indent=4, ensure_ascii=False) + "\n", encoding="utf-8")


def delete_ticket_file(ticket_number: str, filename: str) -> None:
    path = Path("plato-workspace/tickets") / ticket_number / filename
    if path.exists():
        path.unlink()
        print(f"deleted {path.as_posix()}")


def set_entry_status(ticket_number: str, key: str, status: str, session_id: str | None = None) -> None:
    path, data = load_status(ticket_number)
    entry = data.setdefault(key, {})
    entry["status"] = status
    if session_id is not None:
        entry["session-id"] = session_id
    save_status(path, data)
    print(f"{key} in ticket {ticket_number} set to {status}")
