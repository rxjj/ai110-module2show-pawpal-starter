# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each? 

The three main actions in PawPal+ are:
1. Add pet information, such as name and species.
2. Add care tasks, including duration and priority.
3. Generate a daily schedule based on task priority and available time.

My initial UML design includes four classes: Owner, Pet, Task, and Scheduler.

- The Owner class stores the owner's information and pets. The Pet class stores pet information and tasks. The Task class stores duration and priority. The Scheduler class creates a daily schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

- My design grew during implementation. I kept the four main classes, but added more details to support the features I built. Tasks now include a completion status, frequency, optional start time, and optional due date. The Pet class can complete daily or weekly tasks and create their next occurrence. The Scheduler can sort tasks by start time, filter by pet or completion status, find scheduling conflicts, and generate and explain a schedule. I also updated my UML diagram to match these classes, methods, and relationships.


---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

- The scheduler uses the available minutes as a limit. It considers valid, incomplete tasks, looks at higher-priority tasks first, and considers shorter tasks first when priorities are equal. It adds a task only if it fits in the remaining time. Completed or invalid tasks are left out. Start times are used for sorting and conflict detection, but not to place tasks into time slots in the generated schedule. I focused on available time and priority because they determine which care tasks can fit into the day's plan.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

- I decided to keep the current conflict detection method because it is easier to understand. It checks each pair of tasks to see if their scheduled times overlap. Copilot suggested sorting the tasks first to improve performance, but that would make the code more complicated. Since PawPal+ is a small pet care scheduling app, I think keeping the code simple and readable is more important than optimizing its performance right now.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

- I used GitHub Copilot to help design my UML diagram and implement the four Python classes: Owner, Pet, Task, and Scheduler. It also helped with the demo script, tests, project documentation, and connecting the scheduler to the Streamlit interface. The most helpful prompts were specific instructions explaining what each class or method should do. This made it easier to build the project step by step.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

- I reviewed GitHub Copilot's suggestions instead of accepting them automatically. For example, I kept conflict detection as a simple pair-by-pair check rather than adding a more complicated optimization. I checked the code against the project requirements and verified that the Scheduler collects tasks from all pets. I ran the Streamlit app and confirmed it started successfully, ran `python3 main.py` to inspect the demo output, and ran `python3 -m pytest`. All 9 automated tests passed.


---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

- I tested adding a task, marking a task complete, sorting tasks by time, creating daily and weekly recurring tasks, preventing a duplicate recurring task, and detecting overlapping tasks while ignoring non-overlaps. These tests are important because they check the main task and scheduling behaviors. I ran `python3 -m pytest`, and all 9 automated tests passed. Filtering and schedule generation are implemented, but are not directly covered by the current automated tests.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

- I am 4 out of 5 confident that my scheduler works. The app started successfully, and the 9 automated tests passed for the behaviors they cover. Additional edge cases could still be tested, such as invalid times, several tasks overlapping at once, and more combinations of task durations and available time.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

- I am most satisfied with getting the scheduling system to work. I was able to add pets and tasks, organize schedules, and detect conflicts. It was great seeing the different parts of my project work together.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

- If I had more time, I would improve the user interface and make the scheduling system easier to use. I would also add more tests and improve how recurring tasks are managed.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?

- One important thing I learned is that AI can help with coding, but I still need to understand and test the results. Breaking the project into smaller steps made it easier to build and troubleshoot.
