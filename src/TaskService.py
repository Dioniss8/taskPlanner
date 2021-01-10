from src.Db import DataBase


class TaskService:

    def __init__(self):
        self.databaseRepo = DataBase()

    def getAllTasks(self):
        return self.databaseRepo.getAllTasks()

    def addTaskAndReturnAll(self, task):
        self.databaseRepo.setTask(task)

        return self.getAllTasks()

    def deleteTaskById(self, taskId):
        self.databaseRepo.deleteTask(taskId)

    def getPreviousTaskById(self, taskId):
        task = self.databaseRepo.getTaskById(taskId)[0]
        previous = task["description"]

        return {"previous": previous,
                "taskId": taskId}

    def saveNewValueByTaskId(self, newVal, taskId):
        self.databaseRepo.saveDescription(newVal, taskId)
