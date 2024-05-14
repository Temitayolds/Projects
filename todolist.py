import datetime
import time
import threading

class Task:
    def __init__(self, description, start_time=None, end_time=None):
        self.description = description
        self.start_time = start_time
        self.end_time = end_time

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print("Task added successfully!")

    def view_tasks(self):
        if not self.tasks:
            print("No tasks in the list.")
        else:
            print("Tasks:")
            for idx, task in enumerate(self.tasks, start=1):
                print(f"{idx}. {task.description} - Start: {task.start_time}, End: {task.end_time}")

    def remove_task(self, task_index):
        if task_index < 1 or task_index > len(self.tasks):
            print("Invalid task index.")
        else:
            removed_task = self.tasks.pop(task_index - 1)
            print(f"Task '{removed_task.description}' removed successfully.")

    def check_due_tasks(self):
        current_time = datetime.datetime.now()
        for task in self.tasks:
            if task.start_time and task.end_time:
                if task.start_time <= current_time <= task.end_time:
                    print(f"ALARM: It's time to start/continue task '{task.description}'!")
            elif task.start_time:
                if task.start_time <= current_time:
                    print(f"ALARM: It's time to start task '{task.description}'!")
            elif task.end_time:
                if current_time <= task.end_time:
                    print(f"ALARM: It's time to end task '{task.description}'!")

def periodic_check(todo_list):
    while True:
        todo_list.check_due_tasks()
        time.sleep(1)

def main():
    todo_list = ToDoList()
    
    # Start a separate thread for periodic checking
    threading.Thread(target=periodic_check, args=(todo_list,), daemon=True).start()

    while True:
        print("\n1. Add Task")
        print("2. View Tasks")
        print("3. Remove Task")
        print("4. Exit")

        choice = input("Enter your choice:")

        if choice == '1':
            task_description = input("Enter task description: ")
            start_time_str = input("Enter start time (optional, format: HH:MM): ")
            end_time_str = input("Enter end time (optional, format: HH:MM): ")
            start_time = None
            end_time = None
            if start_time_str:
                start_time = datetime.datetime.strptime(start_time_str, '%H:%M').replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
            if end_time_str:
                end_time = datetime.datetime.strptime(end_time_str, '%H:%M').replace(year=datetime.datetime.now().year, month=datetime.datetime.now().month, day=datetime.datetime.now().day)
            task = Task(description=task_description, start_time=start_time, end_time=end_time)
            todo_list.add_task(task)
        elif choice == '2':
            todo_list.view_tasks()
        elif choice == '3':
            if not todo_list.tasks:
                print("No tasks to remove.")
            else:
                task_index = int(input("Enter the index of the task to remove: "))
                todo_list.remove_task(task_index)
        elif choice == '4':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
