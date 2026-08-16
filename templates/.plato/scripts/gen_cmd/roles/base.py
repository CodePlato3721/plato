from abc import ABC, abstractmethod


class RoleStrategy(ABC):
    role_file: str

    @abstractmethod
    def build_start_command(self, session_id: str, ticket_number: str, task_id: str) -> str: ...

    def build_resume_command(self, session_id: str) -> str:
        return f'claude --dangerously-skip-permissions --resume "{session_id}"'

    def get_command(self, status: str, session_id: str, ticket_number: str, task_id: str) -> str:
        if status == "TODO":
            return self.build_start_command(session_id, ticket_number, task_id)
        if status in ("IN_PROGRESS", "WAITING"):
            return self.build_resume_command(session_id)
        raise ValueError(f"unexpected status: {status}")
