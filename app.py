import streamlit as st


from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

You will design and implement the scheduling logic and connect it to this Streamlit UI.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Owner")
owner_name = st.text_input("Owner name", value="Jordan")
if "owner" not in st.session_state:
    st.session_state.owner = Owner(name=owner_name, available_time="Not specified")
else:
    st.session_state.owner.name = owner_name

owner = st.session_state.owner

st.markdown("### Add a Pet")
with st.form("add_pet_form"):
    pet_name = st.text_input("Pet name", value="Mochi")
    species = st.selectbox("Species", ["dog", "cat", "other"])
    add_pet = st.form_submit_button("Add pet")

if add_pet:
    owner.add_pet(Pet(name=pet_name, species=species))
    st.success(f"Added {pet_name}!")

st.markdown("### Your Pets")
if owner.pets:
    for pet in owner.pets:
        st.write(f"**{pet.name}** ({pet.species})")
else:
    st.info("No pets yet. Add a pet above.")

st.markdown("### Add a Task")
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
        add_task = st.form_submit_button("Add task")

    if add_task:
        task = Task(
            title=task_title,
            duration_minutes=int(duration),
            priority=priority_values[priority_label],
            frequency=frequency,
        )
        selected_pet = owner.pets[selected_pet_index]
        selected_pet.add_task(task)
        st.success(f"Added task to {selected_pet.name}!")

    for pet in owner.pets:
        if pet.tasks:
            st.write(f"**{pet.name}'s tasks:**")
            st.table(
                [
                    {
                        "Title": task.title,
                        "Duration (minutes)": task.duration_minutes,
                        "Priority": task.priority,
                        "Frequency": task.frequency,
                        "Completed": task.completed,
                    }
                    for task in pet.tasks
                ]
            )
else:
    st.info("Add a pet before adding tasks.")

st.divider()

st.subheader("Build Schedule")
available_minutes = st.number_input(
    "Available time today (minutes)",
    min_value=0,
    max_value=1440,
    value=60,
)

if st.button("Generate schedule"):
    owner = st.session_state.owner
    scheduler = Scheduler(owner, available_minutes=int(available_minutes))
    daily_schedule = scheduler.generate_schedule()

    st.markdown("### Today's Schedule")
    st.text(daily_schedule)
