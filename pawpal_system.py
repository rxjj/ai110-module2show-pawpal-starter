from __future__ import annotations

from dataclasses import dataclass, field


class Owner:
    def __init__(self, name: str, available_time: str) -> None:
        """Set up an owner and an empty list of pets."""
        self.name = name
        self.available_time = available_time
        self.pets: list[Pet] = []

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> list[Task]:
        """Return the tasks belonging to all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


@dataclass
class Pet:
    name: str
    species: str
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a care task to this pet's task list."""
        self.tasks.append(task)


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    frequency: str = "daily"
    completed: bool = False

    def is_valid(self) -> bool:
        """Check that the task has a title and valid task details."""
        return (
            bool(self.title.strip())
            and self.duration_minutes > 0
            and bool(self.frequency.strip())
            and self.priority > 0
        )

    def mark_complete(self) -> None:
        """Mark this task as completed."""
        self.completed = True


class Scheduler:
    def __init__(self, owner: Owner, available_minutes: int) -> None:
        """Set up a scheduler for an owner and their available minutes."""
        self.owner = owner
        self.tasks = owner.get_all_tasks()
        self.available_minutes = available_minutes

    def generate_schedule(self) -> str:
        """Create a readable schedule from tasks that fit the available time."""
        self.tasks = self.owner.get_all_tasks()
        total_available_minutes = max(0, self.available_minutes)
        remaining_minutes = total_available_minutes
        scheduled_tasks: list[Task] = []

        tasks_by_priority = sorted(
            self.tasks,
            key=lambda task: (-task.priority, task.duration_minutes),
        )

        for task in tasks_by_priority:
            if task.completed or not task.is_valid():
                continue
            if task.duration_minutes <= remaining_minutes:
                scheduled_tasks.append(task)
                remaining_minutes -= task.duration_minutes

        if not scheduled_tasks:
            return "No tasks fit into today's available time."

        lines = ["Daily schedule:"]
        for task in scheduled_tasks:
            lines.append(
                f"- {task.title} ({task.duration_minutes} min, "
                f"priority {task.priority}, {task.frequency})"
            )
        lines.append(
            f"Total: {total_available_minutes - remaining_minutes} of "
            f"{total_available_minutes} minutes"
        )
        return "\n".join(lines)

    def explain_plan(self) -> str:
        """Describe how tasks are chosen for the schedule."""
        return (
            "Tasks are considered from highest to lowest priority. "
            "Tasks with the same priority are considered from shortest to "
            "longest, and completed or invalid tasks are left out. "
            "A task is scheduled only if it fits in the remaining time."
        )