"""Domain models and simple DTOs."""


class Task:
    def __init__(self, title: str, payload: dict | None = None):
        self.title = title
        self.payload = payload or {}
