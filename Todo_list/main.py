from tasks import add_task, remove_task, list_tasks, initialize_weekly_tasks
from user_interface import display_menu, get_user_choice, prompt_for_task, prompt_for_day
from storage import load_tasks, save_tasks

def main():
    tasks = load_tasks()
    if not tasks:
        tasks = initialize_weekly_tasks()

    while True:
        display_menu()
        choice = get_user_choice()

        if choice == "1":
            day = prompt_for_day()
            task = prompt_for_task()
            add_task(tasks, day, task)
        elif choice == "2":
            day = prompt_for_day()
            task = prompt_for_task()
            remove_task(tasks, day, task)
        elif choice == "3":
            list_tasks(tasks)
        elif choice == "4":
            save_tasks(tasks)
            break
        else:
            print("Invalid choice. Please try again.")

    save_tasks(tasks)

if __name__ == "__main__":
    main()
