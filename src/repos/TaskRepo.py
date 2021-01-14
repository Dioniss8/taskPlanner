from src.repos.BaseRepo import BaseRepo
from datetime import datetime

DEFAULT_DELETED = 0
DEFAULT_DONE = 0


class TaskRepo(BaseRepo):

    def __init__(self):
        super().__init__()

    def getAllTasks(self, user_id):
        tasks = self.db.execute('''SELECT * 
                                    FROM tasks 
                                    WHERE deleted = 0
                                    AND user_id=:user_id''',
                                user_id=user_id)

        return tasks

    def setTask(self, description, user_id):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("""INSERT INTO tasks (description, done, deleted, created_at, user_id)
                            VALUES (:description, :done, :deleted, :created_at, :user_id)""",
                        description=description, done=DEFAULT_DONE,
                        deleted=DEFAULT_DELETED, created_at=created_at,
                        user_id=user_id)

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
                            SET description = :text
                            WHERE id=:taskId""",
                        text=text, taskId=taskId)
