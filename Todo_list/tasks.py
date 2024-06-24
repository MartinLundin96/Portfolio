DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def initialize_weekly_tasks():
    return {day: [] for day in DAYS_OF_WEEK} 

def add_task(tasks, day, task):
    tasks[day].append(task)
    print(f"Task '{task}' added to {day}.")

def remove_task(tasks, day, task):
    if task in tasks[day]:
        tasks[day].remove(task)
        print(f"Task '{task}' removed from {day}.")
    else:
        print(f"Task '{task}' not found on {day}.")

def list_tasks(tasks):
    for day, day_tasks in tasks.items():
        print(f"\n{day}:")
        if day_tasks:
            for task in day_tasks:
                print(f"- {task}")
        else:
            print("No tasks")

