from src.Db import UserRepo


class TaskService:

    def __init__(self):
        self.databaseRepo = UserRepo()

    def getAllTasks(self, user_id):
        return self.databaseRepo.getAllTasks(user_id)

    def addTaskAndReturnAll(self, task, user_id):
        self.databaseRepo.setTask(task, user_id)

        return self.getAllTasks(user_id)

    def deleteTaskById(self, taskId):
        self.databaseRepo.deleteTask(taskId)

    def getPreviousTaskById(self, taskId):
        task = self.databaseRepo.getTaskById(taskId)[0]
        previous = task["description"]

        return {"previous": previous,
                "taskId": taskId}

    def saveNewValueByTaskId(self, newVal, taskId):
        self.databaseRepo.saveDescription(newVal, taskId)
