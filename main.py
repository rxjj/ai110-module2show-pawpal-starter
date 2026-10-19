from pawpal_system import Owner, Pet, Scheduler, Task


def main() -> None:
    owner = Owner(name="Alex", available_time="Morning")

    dog = Pet(name="Milo", species="Dog")
    cat = Pet(name="Luna", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)

    dog.add_task(Task("Walk Milo", duration_minutes=30, priority=3))
    dog.add_task(Task("Feed Milo", duration_minutes=10, priority=2))
    cat.add_task(Task("Play with Luna", duration_minutes=15, priority=2))
    cat.add_task(Task("Feed Luna", duration_minutes=10, priority=3))

    scheduler = Scheduler(owner, available_minutes=65)

    print("Today's Schedule")
    print(scheduler.generate_schedule())


if __name__ == "__main__":
    main()