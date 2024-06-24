import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QLabel, QListWidget, QLineEdit,
    QPushButton, QVBoxLayout, QWidget, QDialog, QMessageBox, QListWidgetItem, QTextEdit
)
from PyQt5.QtCore import Qt
from tasks import add_task, remove_task, initialize_weekly_tasks
from storage import load_tasks, save_tasks

class CustomPopup(QDialog):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Message")
        self.label = QLabel(message)
        self.label.setAlignment(Qt.AlignCenter)

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

class TodoListApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weekly Todo List")

        self.tasks = load_tasks()  # Load tasks from tasks.json

        if not self.tasks:
            self.tasks = initialize_weekly_tasks()
            self.show_popup("Initialized new weekly tasks.")

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)

        label = QLabel("Weekly Todo List", self)
        font = label.font()
        font.setBold(True)
        label.setFont(font)
        layout.addWidget(label)

        self.listbox = QListWidget(self)
        self.listbox.itemClicked.connect(self.on_item_clicked)  # Connect itemClicked signal
        layout.addWidget(self.listbox)

        self.task_entry = QLineEdit(self)
        self.task_entry.setPlaceholderText("Enter task")
        layout.addWidget(self.task_entry)

        add_button = QPushButton("Add Task", self)
        add_button.clicked.connect(self.add_task)
        layout.addWidget(add_button)

        remove_button = QPushButton("Remove Task", self)
        remove_button.clicked.connect(self.remove_task)
        layout.addWidget(remove_button)

        clear_button = QPushButton("Clear Tasks", self)
        clear_button.clicked.connect(self.clear_tasks)
        layout.addWidget(clear_button)

        save_button = QPushButton("Save Tasks", self)
        save_button.clicked.connect(self.save_tasks)
        layout.addWidget(save_button)

        quit_button = QPushButton("Quit", self)
        quit_button.clicked.connect(self.close)
        layout.addWidget(quit_button)

        # TextEdit widget to display tasks
        self.task_display = QTextEdit(self)
        self.task_display.setReadOnly(True)  # Make it read-only
        layout.addWidget(self.task_display)

        self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.clear()
        for day, day_tasks in self.tasks.items():
            item = QListWidgetItem(day)
            item.setData(Qt.UserRole, day)  # Store day in UserRole for later retrieval
            self.listbox.addItem(item)

    def add_task(self):
        selected_items = self.listbox.selectedItems()
        if selected_items:
            day = selected_items[0].data(Qt.UserRole)
            task = self.task_entry.text().strip()
            if task:
                add_task(self.tasks, day, task)
                self.refresh_listbox()
                self.update_task_display(day)  # Update task display for the selected day
                self.task_entry.clear()
                self.task_entry.setFocus()
            else:
                self.show_popup("Please enter a task.")
        else:
            self.show_popup("Please select a day.")

    def remove_task(self):
        selected_items = self.listbox.selectedItems()
        if selected_items:
            day = selected_items[0].data(Qt.UserRole)
            task_text = selected_items[0].text()
            task = task_text.split(": ")[1]  # Extract task from item text
            remove_task(self.tasks, day, task)
            self.refresh_listbox()
            self.update_task_display(day)  # Update task display for the selected day

    def clear_tasks(self):
        self.tasks = initialize_weekly_tasks()
        self.refresh_listbox()
        self.task_display.clear()

    def save_tasks(self):
        save_tasks(self.tasks)
        self.show_popup("Tasks saved.")

    def show_popup(self, message):
        popup = CustomPopup(message)
        popup.exec_()

    def on_item_clicked(self, item):
        # Populate task entry when a day is clicked
        day = item.data(Qt.UserRole)
        self.update_task_display(day)
        self.task_entry.clear()
        self.task_entry.setFocus()

    def update_task_display(self, day):
        # Update task display with tasks for the selected day
        if day in self.tasks:
            tasks = "\n".join(self.tasks[day])
            self.task_display.setPlainText(f"{day} Tasks:\n\n{tasks}")
        else:
            self.task_display.clear()

def main():
    app = QApplication(sys.argv)
    window = TodoListApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
