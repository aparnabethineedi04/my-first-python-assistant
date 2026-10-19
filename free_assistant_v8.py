
import json
from pathlib import Path 
from datetime import datetime
from agent_tools import search_notes

TASKS_FILE = Path(__file__).with_name("tasks.json")


def load_tasks():
    if not TASKS_FILE.exists():
        return []

    try:
        with TASKS_FILE.open("r", encoding="utf-8") as file:
            tasks = json.load(file)

        return tasks if isinstance(tasks, list) else []

    except (json.JSONDecodeError, OSError):
        print("Agent: Could not read the task file.")
        return []


def save_tasks(tasks):
    with TASKS_FILE.open("w", encoding="utf-8") as file:
        json.dump(tasks, file, indent=4)


def show_tasks(tasks):
    if not tasks:
        print("Agent: You have no tasks yet.")
        return

    for number, task in enumerate(tasks, start=1):
        status = "Done" if task["done"] else "Pending"
        print(f"{number}. [{status}] {task['title']}")


def make_plan(goal):
    goal = goal.lower().strip()

    if "python" in goal:
        return [
            "Learn Python variables and data types",
            "Practise if and else conditions",
            "Learn for loops and while loops",
            "Write simple Python programs",
            "Practise Python problems"
        ]

    elif "job" in goal:
        return [
            "Prepare or update your resume",
            "Practise Python interview questions",
            "Practise SQL interview questions",
            "Prepare to explain your projects",
            "Apply for suitable jobs"
        ]

    elif "project" in goal:
        return [
            "Choose the project goal",
            "List the required features",
            "Break the project into small tasks",
            "Build and test each feature",
            "Review and improve the project"
        ]

    else:
        return [
            "Write down the main goal",
            "Identify the first small step",
            "Complete the first step",
            "Review your progress",
            "Decide the next step"
        ]


tasks = load_tasks()

print("Welcome to your Python Planning Assistant!")
print("Type help to see the commands.")

while True:
    message = input("\nYou: ").strip()
    command = message.lower()

    if command == "bye":
        print("Agent: Goodbye!")
        break
    elif command == "time":
        current_time = datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
        print("Agent: The current date and time is", current_time)
    elif command == "read file":
        file_path = Path(__file__).with_name("my_notes.txt")

        try:
            content = file_path.read_text(encoding="utf-8")
            print("Agent: Here is your file content:")
            print(content)
        except OSError:
            print("Agent: Sorry, I could not read the file.")
    elif command.startswith("search notes "):
        keyword = message[len("search notes "):].strip()
        results = search_notes(keyword)

        print("Agent: Here are the matching notes:")
        for note in results:
            print("-", note)
    elif command == "help":
               print("\n--- MY PYTHON ASSISTANT ---")
               print("1. plan <goal>       - Create a plan")
               print("2. add task <text>   - Add a task")
               print("3. show tasks        - View saved tasks")
               print("4. done <number>     - Complete a task")
               print("5. search notes <word> - Search saved notes")
               print("6. read file         - Read my notes file")
               print("7. time              - Show date and time")
               print("8. bye               - Exit assistant")

    elif command.startswith("plan "):
        goal = message[5:].strip()

        if not goal:
            print("Agent: Please tell me your goal.")
            continue

        plan_steps = make_plan(goal)

        print("\nAgent: Here is your plan:")
        for number, step in enumerate(plan_steps, start=1):
            print(f"{number}. {step}")

        answer = input(
            "\nAgent: Save these steps as tasks? (yes/no): "
        ).strip().lower()

        if answer == "yes":
            for step in plan_steps:
                tasks.append({"title": step, "done": False})

            save_tasks(tasks)
            print("Agent: Plan saved as tasks!")

        else:
            print("Agent: No tasks were added.")

    
    elif command.startswith("add task "):
        title = message[len("add task "):].strip()

        if not title:
            print("Agent: Please enter a task description.")
            continue

        if any(
            task["title"].strip().lower() == title.lower()
            for task in tasks
        ):
            print("Agent: This task already exists.")
            continue

        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        print("Agent: Task saved successfully.")


    elif command == "show tasks":
        show_tasks(tasks)

    elif command.startswith("done "):
        parts = command.split()

        if len(parts) != 2 or not parts[1].isdigit():
            print("Agent: Try: done 1")
            continue

        number = int(parts[1])

        if 1 <= number <= len(tasks):
            tasks[number - 1]["done"] = True
            save_tasks(tasks)
            print("Agent: Task marked as completed.")
        else:
            print("Agent: That task number does not exist.")

    else:
        print("Agent: I don't know that command.")
        print("Agent: Type help to see available commands.")
