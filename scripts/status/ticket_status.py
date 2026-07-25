import json
from pathlib import Path


class TicketStatus:
    def __init__(self, ticket_number: str):
        self.ticket_number = ticket_number
        self._path = Path("plato-workspace/tickets") / ticket_number / "status.json"

    def exists(self) -> bool:
        return self._path.exists()

    def read(self) -> dict:
        raw = json.loads(self._path.read_text(encoding="utf-8"))
        result = {
            "ticket_number": self.ticket_number,
            "type": raw.get("type", ""),
            "title": raw.get("title", ""),
        }

        if result["type"] == "defect":
            result["fixer"] = raw.get("fixer", {}).get("status", "")
            return result

        tasks = raw.get("coder", {}).get("tasks", [])
        result["designer"] = raw.get("designer", {}).get("status", "")
        result["planner"] = raw.get("planner", {}).get("status", "")
        result["coder"] = raw.get("coder", {}).get("status", "")
        result["tasks"] = [{"id": t.get("id", ""), "status": t.get("status", "")} for t in tasks]
        return result
