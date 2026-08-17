from .base import RoleStrategy


class PlannerStrategy(RoleStrategy):
    role_file = ".plato/planner/PLANNER.md"

    def build_start_command(self, session_id: str, ticket_number: str, _task_id: str) -> str:
        prompt = f"ticket-number={ticket_number}, session-id={session_id}"
        return f'claude --dangerously-skip-permissions --session-id "{session_id}" --append-system-prompt-file "{self.role_file}" "{prompt}"'
