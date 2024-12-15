#This particular project highlights my understanding of the basics of python programming, including the basic syntax
# handling of files, as well basics object-oriented programming. Now, there is enough foundation for me to get into Data Science and ML

#Task Manager Project

class Task:
    def __init__(self, task_name, task_description, due_date):
        self.task_name = task_name
        self.task_description = task_description
        self.due_date = due_date
        self.status = False

    def __str__(self):
        status_str = "Completed" if self.status else "Not Completed"
        return f"{self.task_name} - Due: {self.due_date} - {status_str}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_tasks()

    def write_files(self):
        with open("storage.txt", "w") as file:
            for item in self.tasks:
                line = f"{item.task_name};{item.task_description};{item.due_date};{item.status}\n"
                file.write(line)

    def load_tasks(self):
        try:
            with open("storage.txt") as file:
                for line in file:
                    name, description, due_date, status = line.strip().split(";")
                    task = Task(name, description, due_date)
                    task.status = status.lower() == 'true'
                    self.tasks.append(task)
        except FileNotFoundError:
            pass

    def add_task(self, task: Task):
        if task.task_name not in {t.task_name for t in self.tasks}:
            self.tasks.append(task)
            self.write_files()
        else:
            print(f"Task with name '{task.task_name}' already exists.")

    def task_remove(self, tk_name):
        self.tasks = [task for task in self.tasks if task.task_name != tk_name]
        self.write_files()

    def completed(self, tk_name):
        for task in self.tasks:
            if task.task_name == tk_name:
                task.status = True
                self.write_files()

    def show_due_tasks(self):
        result = [task for task in self.tasks if not task.status]
        return result

    def completed_tasks(self):
        result = [task for task in self.tasks if task.status]
        return result

    def show_all_tasks(self):
        return self.tasks
    
    def clear_everything(self):
        self.tasks = []
        self.write_files()


def UserInterface():
    manager = TaskManager()

    while True:
        print("0-exit")
        print("1-Add task")
        print("2-Mark completed")
        print("3-Remove task")
        print("4-Show due tasks")
        print("5-Show completed tasks")
        print("6-Show all tasks")
        print("7-To remove all the tasks")

        user = int(input("Provide a number: "))
        if user == 0:
            manager.write_files()
            break
        elif user == 1:
            name = input("Task name: ")
            description = input("Task description: ")
            date = input("Due Date: ")

            task = Task(name, description, date)
            manager.add_task(task)
            print("Task added successfully")

        elif user == 2:
            name = input("Which task did you finally complete: ")
            manager.completed(name)

        elif user == 3:
            name = input("Which task do you want to remove? ")
            manager.task_remove(name)

        elif user == 4:
            print("Your due tasks are following:")
            for task in sorted(manager.show_due_tasks(), key=lambda t: t.due_date):
                print(task)

        elif user == 5:
            print("Your completed tasks are:")
            for task in sorted(manager.completed_tasks(), key=lambda t: t.due_date):
                print(task)

        elif user == 6:
            print("All the completed and uncompleted tasks in the system: ")
            for task in sorted(manager.show_all_tasks(), key=lambda t: t.due_date):
                print(task)

        elif user == 7:
            print("Press 1 for yes, 0 for no")
            another_input = int(input("Are you sure you want to remove everything? "))
            if another_input == 0:
                manager.write_files()
                break
            else:
                manager.clear_everything()


if __name__ == "__main__":
    UserInterface()
