from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


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

    def mark_task_complete(
        self,
        task: Task,
        completed_on: date | None = None,
    ) -> Task | None:
        """Finish a task and add its next daily or weekly copy."""
        if not any(existing_task is task for existing_task in self.tasks):
            raise ValueError("The task does not belong to this pet.")
        if task.completed:
            return None

        task.mark_complete()
        frequency = task.frequency.strip().casefold()
        if frequency == "daily":
            recurrence = timedelta(days=1)
        elif frequency == "weekly":
            recurrence = timedelta(days=7)
        else:
            return None

        if completed_on is not None:
            occurrence_date = completed_on
        elif task.due_date is not None:
            occurrence_date = task.due_date
        else:
            occurrence_date = date.today()
        next_due_date = occurrence_date + recurrence

        for existing_task in self.tasks:
            if (
                existing_task.title == task.title
                and existing_task.duration_minutes == task.duration_minutes
                and existing_task.priority == task.priority
                and existing_task.frequency.strip().casefold() == frequency
                and existing_task.start_time == task.start_time
                and existing_task.due_date == next_due_date
            ):
                return existing_task

        next_task = Task(
            title=task.title,
            duration_minutes=task.duration_minutes,
            priority=task.priority,
            frequency=task.frequency,
            start_time=task.start_time,
            due_date=next_due_date,
        )
        self.add_task(next_task)
        return next_task


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: int
    frequency: str = "daily"
    completed: bool = False
    start_time: str | None = None
    due_date: date | None = None

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

    def sort_by_time(self) -> list[Task]:
        """List tasks from earliest start time to latest, untimed tasks last."""
        tasks = self.owner.get_all_tasks()
        return sorted(
            tasks,
            key=lambda task: (task.start_time is None, task.start_time or ""),
        )

    def filter_tasks(
        self,
        completed: bool | None = None,
        pet_name: str | None = None,
    ) -> list[Task]:
        """List tasks that match the chosen pet name and completion status."""
        if pet_name is None:
            tasks = self.owner.get_all_tasks()
        else:
            tasks = [
                task
                for pet in self.owner.pets
                if pet.name.casefold() == pet_name.casefold()
                for task in pet.tasks
            ]

        if completed is not None:
            tasks = [task for task in tasks if task.completed == completed]
        return tasks

    def find_conflicts(self) -> list[str]:
        """Find and describe overlapping scheduled tasks."""
        timed_tasks: list[tuple[Pet, Task, int]] = []
        for pet in self.owner.pets:
            for task in pet.tasks:
                if task.completed or task.start_time is None:
                    continue
                if task.duration_minutes <= 0:
                    continue

                time_parts = task.start_time.split(":")
                if len(time_parts) != 2:
                    continue
                try:
                    hours = int(time_parts[0])
                    minutes = int(time_parts[1])
                except ValueError:
                    continue
                if not 0 <= hours < 24 or not 0 <= minutes < 60:
                    continue

                start_minutes = hours * 60 + minutes
                timed_tasks.append((pet, task, start_minutes))

        warnings: list[str] = []
        for index, (pet, task, start_minutes) in enumerate(timed_tasks):
            task_end = start_minutes + task.duration_minutes
            for other_pet, other_task, other_start in timed_tasks[index + 1 :]:
                if (
                    task.due_date is not None
                    and other_task.due_date is not None
                    and task.due_date != other_task.due_date
                ):
                    continue

                other_end = other_start + other_task.duration_minutes
                if start_minutes < other_end and other_start < task_end:
                    warnings.append(
                        f"Conflict: {pet.name}'s {task.title} "
                        f"({task.start_time}-{task_end // 60:02d}:"
                        f"{task_end % 60:02d}) overlaps "
                        f"{other_pet.name}'s {other_task.title} "
                        f"({other_task.start_time}-{other_end // 60:02d}:"
                        f"{other_end % 60:02d})."
                    )
        return warnings

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