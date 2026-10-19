from pawpal_system import Pet, Task


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