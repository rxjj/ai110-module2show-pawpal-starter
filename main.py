from datetime import date

from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Alex", available_time="Morning")

    dog = Pet(name="Milo", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(
        Task("Walk Milo", duration_minutes=30, priority=3, start_time="08:00")
    )
    dog.add_task(
        Task("Feed Milo", duration_minutes=10, priority=2, start_time="07:30")
    )
    cat.add_task(
        Task("Play with Luna", duration_minutes=15, priority=2, start_time="09:00")
    )
    cat.add_task(
        Task("Feed Luna", duration_minutes=10, priority=3, start_time="07:00")
    )
    cat.add_task(
        Task("Prepare for vet visit", duration_minutes=20, priority=2, start_time="08:15")
    )
    daily_task = Task(
        "Brush Milo",
        duration_minutes=10,
        priority=1,
        start_time="10:00",
        due_date=date.today(),
    )
    dog.add_task(daily_task)
    next_daily_task = dog.mark_task_complete(daily_task)

    weekly_task = Task(
        "Give Luna flea prevention",
        duration_minutes=5,
        priority=1,
        frequency="weekly",
        due_date=date.today(),
    )
    cat.add_task(weekly_task)
    next_weekly_task = cat.mark_task_complete(weekly_task)

    print("Recurring tasks")
    if next_daily_task is not None and next_daily_task.due_date is not None:
        print(f"- {next_daily_task.title}: {next_daily_task.due_date} (daily)")
    if next_weekly_task is not None and next_weekly_task.due_date is not None:
        print(f"- {next_weekly_task.title}: {next_weekly_task.due_date} (weekly)")

    scheduler = Scheduler(owner, available_minutes=65)

    print("Scheduling conflicts")
    conflict_warnings = scheduler.find_conflicts()
    if conflict_warnings:
        for warning in conflict_warnings:
            print(f"- {warning}")
    else:
        print("No scheduling conflicts found.")

    print("Tasks sorted by time")
    for task in scheduler.sort_by_time():
        print(
            f"- {task.due_date or 'No date'} "
            f"{task.start_time or 'No time'}: {task.title}"
        )

    print("\nMilo's tasks")
    for task in scheduler.filter_tasks(pet_name="Milo"):
        print(f"- {task.title}")

    print("\nCompleted tasks")
    for task in scheduler.filter_tasks(completed=True):
        print(f"- {task.title}")

    print("Today's Schedule")
    print(scheduler.generate_schedule())


if __name__ == "__main__":
    main()