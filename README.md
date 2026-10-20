# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## Implemented features

PawPal+ currently supports:

- Store an owner's name and add pets with a name and species.
- Add care tasks with a title, duration, priority, frequency, and optional start time.
- View all tasks in start-time order, with tasks that have no start time listed last.
- Filter tasks by pet and completion status in the Streamlit app.
- Detect and display overlaps between scheduled tasks.
- Generate a schedule that fits the available minutes, considering higher-priority and shorter tasks first.
- Complete daily or weekly tasks in the Python system to create their next occurrence.
- Explain the schedule selection rules and test core scheduling behaviors.

Task editing and persistent storage are not currently implemented.

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

The following excerpt is from running `python3 main.py`. It demonstrates a
detected overlap and the schedule generated for the 65-minute limit:

```text
Scheduling conflicts
- Conflict: Milo's Walk Milo (08:00-08:30) overlaps Luna's Prepare for vet visit (08:15-08:35).
Today's Schedule
Daily schedule:
- Feed Luna (10 min, priority 3, daily)
- Walk Milo (30 min, priority 3, daily)
- Feed Milo (10 min, priority 2, daily)
- Play with Luna (15 min, priority 2, daily)
Total: 65 of 65 minutes
```

## Testing PawPal+

```bash
python3 -m pytest
```

The 9 automated tests check that tasks can be completed and added, tasks are
sorted by start time, daily and weekly tasks recur correctly, completing a
recurring task twice does not create another copy, and overlapping schedules
are detected while non-overlapping tasks are ignored.

```
9 passed in 0.06s
```

The tests cover adding and completing tasks, time sorting, recurring tasks,
and conflict detection.

## Features

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Pet and task management | `Owner.add_pet()`, `Pet.add_task()` | Add pets and their care tasks. |
| Time sorting | `Scheduler.sort_by_time()` | Lists tasks from earliest start time to latest; tasks without a start time appear last. |
| Filtering | `Scheduler.filter_tasks()` | Finds tasks for a selected pet, by completion status, or by both. |
| Schedule generation | `Scheduler.generate_schedule()` | Selects valid, incomplete tasks that fit within the available minutes, in priority order and then shorter-duration order. |
| Plan explanation | `Scheduler.explain_plan()` | Describes how the scheduler chooses tasks. |
| Recurring tasks | `Pet.mark_task_complete()` | Completing a daily or weekly task creates its next incomplete occurrence, due one or seven days later. |
| Conflict detection | `Scheduler.find_conflicts()` | Finds overlaps between timed, incomplete tasks; the Streamlit app displays each warning. |

## 📸 Demo Walkthrough

To try the interactive app, install the dependencies as described above, then
run:

```bash
streamlit run app.py
```

1. Enter an owner name, or keep the default.
2. In **Your pets**, enter a pet's name, choose its species, and select **Add
   pet**. For example, add Milo as a dog and Luna as a cat.
3. In **Add a task**, choose the pet and enter a task title, duration, priority,
   and frequency. Optionally enter a start time in 24-hour `HH:MM` format.
   For example, add Milo's 30-minute high-priority walk at `08:00`, then add
   Luna's 20-minute medium-priority vet preparation at `08:15`.
4. In **Tasks and schedule**, the task table is sorted by start time
   automatically; untimed tasks appear last. Use the **Pet** and **Status**
   controls to show all pets or one pet, and all, incomplete, or completed
   tasks.
5. The app checks timed tasks for overlaps and displays any conflicts as
   warnings. In this example, Milo's walk and Luna's vet preparation overlap,
   so a warning appears.
6. Set **Available time today** (for example, 65 minutes) and select
   **Generate schedule**. The app displays the selected tasks and a short
   explanation of how they were chosen.

The current Streamlit form adds pets and tasks; it does not provide controls to
mark tasks complete or edit/delete them. Recurring-task completion is
demonstrated by the Python system and `main.py` rather than by a button in the
interactive app. The schedule selects tasks by priority and duration; it does
not schedule them into the entered start-time slots.

## Implementation Summary

PawPal+ is a pet care scheduling system built with Python. It helps owners organize daily tasks for multiple pets.

The system has four classes:

- **Owner:** Stores owner information and manages pets and their tasks.
- **Pet:** Stores pet information and care tasks.
- **Task:** Stores task names, duration, priority, frequency, and completion status.
- **Scheduler:** Sorts and filters tasks, detects overlaps, creates a daily schedule based on priority and available time, and explains its selection rules.

The CLI example in `main.py` creates two pets, adds care tasks, completes daily
and weekly tasks to demonstrate recurrence, shows conflicts, sorts and filters
tasks, and generates a schedule. Run the automated tests with
`python3 -m pytest`.