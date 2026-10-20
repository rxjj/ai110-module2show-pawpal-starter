from datetime import datetime

import streamlit as st

from pawpal_system import Owner, Pet, Scheduler, Task


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")
st.caption("Plan and organize care tasks for your pets.")

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time="Not specified")
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner

st.subheader("Your pets")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name}!")

if owner.pets:
    st.table(
        [{"Name": pet.name, "Species": pet.species} for pet in owner.pets]
    )
else:
    st.info("No pets yet. Add a pet to get started.")

st.subheader("Add a task")
if owner.pets:
    priority_values = {"Low": 1, "Medium": 2, "High": 3}

    with st.form("add_task_form"):
        selected_pet_index = st.selectbox(
            "Choose a pet",
            range(len(owner.pets)),
            format_func=lambda index: (
                f"{owner.pets[index].name} ({owner.pets[index].species})"
            ),
        )
        task_title = st.text_input("Task title", value="Morning walk")
        duration = st.number_input(
            "Duration (minutes)", min_value=1, max_value=240, value=20
        )
        priority_label = st.selectbox("Priority", list(priority_values))
        frequency = st.text_input("Frequency", value="daily")
        task_start_time = st.text_input(
            "Start time (optional, HH:MM)", value="", placeholder="08:00"
        )
        add_task = st.form_submit_button("Add task")

    if add_task:
        start_time = task_start_time.strip() or None
        if start_time is not None:
            try:
                start_time = datetime.strptime(start_time, "%H:%M").strftime(
                    "%H:%M"
                )
            except ValueError:
                st.error("Enter a valid start time in 24-hour HH:MM format.")
                start_time = None
                valid_start_time = False
            else:
                valid_start_time = True
        else:
            valid_start_time = True

        if valid_start_time:
            task = Task(
                title=task_title,
                duration_minutes=int(duration),
                priority=priority_values[priority_label],
                frequency=frequency,
                start_time=start_time,
            )
            selected_pet = owner.pets[selected_pet_index]
            selected_pet.add_task(task)
            st.success(f"Added task to {selected_pet.name}!")
else:
    st.info("Add a pet before adding tasks.")

st.divider()
st.subheader("Tasks and schedule")

available_minutes = st.number_input(
    "Available time today (minutes)",
    min_value=0,
    max_value=1440,
    value=60,
)
scheduler = Scheduler(owner, available_minutes=int(available_minutes))

all_tasks = scheduler.sort_by_time()
if all_tasks:
    st.markdown("### View tasks")
    pet_filter = st.selectbox(
        "Pet",
        ["All pets"] + [pet.name for pet in owner.pets],
    )
    status_filter = st.selectbox(
        "Status",
        ["All tasks", "Incomplete", "Completed"],
    )
    selected_pet = None if pet_filter == "All pets" else pet_filter
    selected_status = {
        "All tasks": None,
        "Incomplete": False,
        "Completed": True,
    }[status_filter]

    filtered_tasks = scheduler.filter_tasks(
        completed=selected_status,
        pet_name=selected_pet,
    )
    filtered_task_ids = {id(task) for task in filtered_tasks}
    tasks_to_show = [
        task for task in all_tasks if id(task) in filtered_task_ids
    ]
    pet_names_by_task_id = {
        id(task): pet.name for pet in owner.pets for task in pet.tasks
    }

    if tasks_to_show:
        st.table(
            [
                {
                    "Start time": task.start_time or "Not set",
                    "Pet": pet_names_by_task_id[id(task)],
                    "Task": task.title,
                    "Duration (minutes)": task.duration_minutes,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Completed": task.completed,
                }
                for task in tasks_to_show
            ]
        )
    else:
        st.info("No tasks match these filters.")

    conflicts = scheduler.find_conflicts()
    if conflicts:
        for conflict in conflicts:
            st.warning(conflict)
    else:
        st.success("No scheduling conflicts found.")
else:
    st.info("Add tasks to see your schedule here.")

if st.button("Generate schedule"):
    daily_schedule = scheduler.generate_schedule()
    if daily_schedule.startswith("No tasks fit"):
        st.info(daily_schedule)
    else:
        st.success(daily_schedule)
    st.caption(scheduler.explain_plan())
