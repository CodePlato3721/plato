import uuid


def prepare_session_id(session_id: str) -> str:
    return session_id if session_id else str(uuid.uuid4())
