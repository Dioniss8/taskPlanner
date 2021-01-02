from cs50 import SQL
from datetime import datetime


class DataBase:
    def __init__(self):
        self.db = SQL("sqlite:///tasks.db")

    def getAllTasks(self):
        tasks = self.db.execute("SELECT * FROM tasks")

        return tasks

    def setTask(self, description):
        done_default = 0
        deleted_default = 0
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("""INSERT INTO tasks (description, done, deleted, created_at)
                            VALUES (:description, :done, :deleted, :created_at)""",
                        description=description, done=done_default,
                        deleted=deleted_default, created_at=created_at)
