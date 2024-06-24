# storage.py

import json

def load_tasks(filename="tasks.json"):
    try:
        with open(filename, "r") as file:
            tasks = json.load(file)
        print("Tasks loaded from", filename)
    except FileNotFoundError:
        tasks = {}
        print("No existing task file found. Starting with an empty task list.")
    except json.JSONDecodeError:
        tasks = {}
        print("Error decoding JSON from the task file. Starting with an empty task list.")
    return tasks

def save_tasks(tasks, filename="tasks.json"):
    try:
        with open(filename, "w") as file:
            json.dump(tasks, file, indent=4)
        print(f"Tasks saved to {filename}")
    except Exception as e:
        print(f"Error saving tasks: {e}")