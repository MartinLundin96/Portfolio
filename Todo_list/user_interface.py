DAYS_OF_WEEK = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

def display_menu():
    print("\nWeekly To-Do List")
    print("1. Add task")
    print("2. Remove task")
    print("3. List tasks")
    print("4. Save and Exit")

def get_user_choice():
    return input("Enter your choice: ")

def prompt_for_task():
    return input("Enter the task: ")

def prompt_for_day():
    print("Choose a day:")
    for i, day in enumerate(DAYS_OF_WEEK, 1):
        print(f"{i}. {day}")
    day_choice = int(input("Enter the number corresponding to the day: "))
    return DAYS_OF_WEEK[day_choice -1]
    