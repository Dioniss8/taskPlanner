from cs50 import SQL
from datetime import datetime

DEFAULT_DONE = 0
DEFAULT_DELETED = 0


class DataBase:
    def __init__(self):
        self.db = SQL("sqlite:///tasks.db")

    def getAllTasks(self):
        tasks = self.db.execute("SELECT * FROM tasks WHERE deleted = 0")

        return tasks

    def setTask(self, description):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("""INSERT INTO tasks (description, done, deleted, created_at)
                            VALUES (:description, :done, :deleted, :created_at)""",
                        description=description, done=DEFAULT_DONE,
                        deleted=DEFAULT_DELETED, created_at=created_at)

    def deleteTask(self, taskId):
        self.db.execute("""UPDATE tasks
                            SET deleted = 1
                            WHERE id=:taskId""", taskId=taskId)

    def getTaskById(self, taskId):
        tasks = self.db.execute("""SELECT *
                            FROM tasks
                            WHERE id=:taskId""", taskId=taskId)

        return tasks

    def saveDescription(self, text, taskId):
        self.db.execute("""UPDATE tasks
                            set description = :text
                            WHERE id=:taskId""", text=text, taskId=taskId)

    def saveCategory(self, name):
        self.db.execute("""INSERT INTO categories (name)
                            VALUES (:name)""", name=name)
