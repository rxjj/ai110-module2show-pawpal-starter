from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def test_mark_complete_sets_task_as_completed() -> None:
    task = Task(title="Feed the dog", duration_minutes=10, priority=1)

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count_by_one() -> None:
    pet = Pet(name="Milo", species="Dog")
    task = Task(title="Walk the dog", duration_minutes=30, priority=2)
    original_task_count = len(pet.tasks)

    pet.add_task(task)

    assert len(pet.tasks) == original_task_count + 1


def test_sort_by_time_puts_tasks_without_a_start_time_last() -> None:
    # Tasks should be sorted from earliest to latest, with untimed tasks last.
    owner = Owner(name="Alex", available_time="Morning")
    pet = Pet(name="Milo", species="Dog")
    owner.add_pet(pet)
    late_task = Task("Evening walk", 20, 1, start_time="18:00")
    untimed_task = Task("Brush fur", 10, 1)
    early_task = Task("Breakfast", 10, 1, start_time="07:30")
    pet.add_task(late_task)
    pet.add_task(untimed_task)
    pet.add_task(early_task)

    scheduler = Scheduler(owner, available_minutes=60)

    assert scheduler.sort_by_time() == [early_task, late_task, untimed_task]


def test_completing_daily_task_creates_next_days_task() -> None:
    # A completed daily task should create an incomplete copy due the next day.
    pet = Pet(name="Milo", species="Dog")
    task = Task(
        "Give medicine",
        5,
        2,
        frequency="daily",
        due_date=date(2025, 1, 31),
    )
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert task.completed is True
    assert next_task is not None
    assert next_task.due_date == date(2025, 2, 1)
    assert next_task.completed is False


def test_completing_weekly_task_creates_task_seven_days_later() -> None:
    # A weekly task should return again exactly seven days after completion.
    pet = Pet(name="Luna", species="Cat")
    task = Task(
        "Flea treatment",
        5,
        1,
        frequency="weekly",
        due_date=date(2025, 12, 29),
    )
    pet.add_task(task)

    next_task = pet.mark_task_complete(task)

    assert next_task is not None
    assert next_task.due_date == date(2026, 1, 5)
    assert next_task.completed is False


def test_completing_the_same_recurring_task_twice_does_not_add_another_copy() -> None:
    # Completing an already completed task should not create a second copy.
    pet = Pet(name="Milo", species="Dog")
    task = Task(
        "Daily walk",
        20,
        2,
        frequency="daily",
        due_date=date(2025, 4, 10),
    )
    pet.add_task(task)

    first_next_task = pet.mark_task_complete(task)
    second_next_task = pet.mark_task_complete(task)

    assert first_next_task is not None
    assert second_next_task is None
    assert len(pet.tasks) == 2


def test_find_conflicts_reports_overlapping_tasks() -> None:
    # Tasks for different pets should be reported when their times overlap.
    owner = Owner(name="Alex", available_time="Morning")
    dog = Pet(name="Milo", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    dog.add_task(Task("Walk", 30, 1, start_time="08:00"))
    cat.add_task(Task("Play", 20, 1, start_time="08:15"))

    warnings = Scheduler(owner, available_minutes=60).find_conflicts()

    assert len(warnings) == 1
    assert "Conflict" in warnings[0]
    assert "Walk" in warnings[0]
    assert "Play" in warnings[0]


def test_find_conflicts_reports_tasks_with_the_same_start_time() -> None:
    # Two tasks starting together overlap and should produce a warning.
    owner = Owner(name="Alex", available_time="Morning")
    pet = Pet(name="Milo", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Breakfast", 10, 1, start_time="08:00"))
    pet.add_task(Task("Medicine", 5, 1, start_time="08:00"))

    warnings = Scheduler(owner, available_minutes=60).find_conflicts()

    assert len(warnings) == 1


def test_find_conflicts_ignores_tasks_that_do_not_overlap() -> None:
    # Back-to-back, untimed, and completed tasks should not create warnings.
    owner = Owner(name="Alex", available_time="Morning")
    pet = Pet(name="Milo", species="Dog")
    owner.add_pet(pet)
    pet.add_task(Task("Breakfast", 30, 1, start_time="08:00"))
    pet.add_task(Task("Walk", 15, 1, start_time="08:30"))
    pet.add_task(Task("Brush fur", 10, 1))
    completed_task = Task("Old task", 10, 1, start_time="08:10", completed=True)
    pet.add_task(completed_task)

    warnings = Scheduler(owner, available_minutes=60).find_conflicts()

    assert warnings == []