import json
import os
from pathlib import Path

class ToDoList:
    def __init__(self, filename="todo_list.json"):
        self.filepath = Path(__file__).parent.parent / filename
        self.tasks = []
        self._load_tasks()

    def _load_tasks(self):
        if self.filepath.exists():
            with open(self.filepath, 'r') as f:
                self.tasks = json.load(f)

    def _save_tasks(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.tasks, f, indent=2)

    def add_task(self, task_text):
        new_task = {
            "id": len(self.tasks) + 1,
            "task": task_text,
            "completed": False,
            "created_at": str(datetime.now())
        }
        self.tasks.append(new_task)
        self._save_tasks()
        return f"Added task: {task_text}"

    def view_tasks(self):
        if not self.tasks:
            return "Your to-do list is empty"
        
        task_list = []
        for task in self.tasks:
            status = "✓" if task["completed"] else "◻"
            task_list.append(f"{task['id']}. {status} {task['task']}")
        return "\n".join(task_list)

    def complete_task(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                self._save_tasks()
                return f"Completed task: {task['task']}"
        return "Task not found"

    def delete_task(self, task_id):
        for idx, task in enumerate(self.tasks):
            if task["id"] == task_id:
                removed = self.tasks.pop(idx)
                self._save_tasks()
                return f"Removed task: {removed['task']}"
        return "Task not found"

    def clear_tasks(self):
        self.tasks = []
        self._save_tasks()
        return "All tasks cleared"