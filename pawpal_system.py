from __future__ import annotations

from dataclasses import dataclass, field


class Owner:
    def __init__(self, name: str, available_time: str) -> None:
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int

    def is_valid(self) -> bool:
        pass


class Scheduler:
    def __init__(self, tasks: list[Task], available_minutes: int) -> None:
        self.tasks = tasks
        self.available_minutes = available_minutes

    def generate_schedule(self) -> list[Task]:
        pass

    def explain_plan(self) -> str:
        pass