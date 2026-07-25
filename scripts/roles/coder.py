from .base import RoleStrategy


class CoderStrategy(RoleStrategy):
    role_file = ".plato/coder/CODER.md"

    def build_start_command(self, session_id: str, ticket_number: str, task_id: str) -> str:
        prompt = f"ticket-number={ticket_number}, task-id={task_id}, session-id={session_id}"
        return f'claude --dangerously-skip-permissions -p --session-id "{session_id}" --append-system-prompt-file "{self.role_file}" "{prompt}"'
