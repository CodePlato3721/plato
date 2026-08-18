import json
from pathlib import Path

from .base import RoleStrategy


class CoderStrategy(RoleStrategy):
    role_file = ".plato/coder/CODER.md"

    def build_start_command(self, session_id: str, ticket_number: str, task_id: str) -> str:
        # coder's prompt shape (task-id or not) is decided by this ticket's status.json
        # `type` field — never inferred from whether task_id happens to be empty.
        status_path = Path("plato-workspace/tickets") / ticket_number / "status.json"
        ticket_type = json.loads(status_path.read_text(encoding="utf-8")).get("type")

        if ticket_type == "simple_feature":
            prompt = f"ticket-number={ticket_number}, session-id={session_id}"
        else:
            prompt = f"ticket-number={ticket_number}, task-id={task_id}, session-id={session_id}"
        return f'claude --dangerously-skip-permissions --session-id "{session_id}" --append-system-prompt-file "{self.role_file}" "{prompt}"'
