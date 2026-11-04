# Each task is a dictionary: {"title": "...", "done": False}
tasks = []


def add_tasks():
    """Ask the user for tasks until they type 'done'."""
    print("Enter your tasks one by one. Type 'done' when you finish.")
    while True:
        title = input("Task: ").strip()
        if title.lower() == "done":
            break
        if title == "":
            print("Task cannot be empty.")
            continue
        tasks.append({"title": title, "done": False})


def show_tasks():
    """Print all tasks with numbers and status."""
    if not tasks:
        print("No tasks yet.")
        return
    for number, task in enumerate(tasks, start=1):
        mark = "[x]" if task["done"] else "[ ]"
        print(f"{number}. {mark} {task['title']}")


def mark_task_done():
    """Let the user mark tasks as completed by their number."""
    if not tasks:
        return
    while True:
        print()
        show_tasks()
        answer = input("Enter the number of a completed task (or 'q' to quit): ").strip()
        if answer.lower() == "q":
            break
        if not answer.isdigit():
            print("Please enter a valid number.")
            continue
        number = int(answer)
        if number < 1 or number > len(tasks):
            print("There is no task with that number.")
            continue
        task = tasks[number - 1]
        if task["done"]:
            print("This task is already marked as done.")
            continue
        task["done"] = True
        print(f"Task completed: {task['title']}")


add_tasks()
mark_task_done()
print()
show_tasks()