from src.repos.TaskRepo import TaskRepo


class TaskService:

    def __init__(self):
        self.taskRepo = TaskRepo()

    def getAllTasks(self, user_id):
        return self.taskRepo.getAllTasks(user_id)

    def addTaskAndReturnAll(self, task, user_id):
        self.taskRepo.setTask(task, user_id)

        return self.getAllTasks(user_id)

    def deleteTaskById(self, taskId):
        self.taskRepo.deleteTask(taskId)

    def getPreviousTaskById(self, taskId):
        task = self.taskRepo.getTaskById(taskId)[0]
        previous = task["description"]

        return {"previous": previous,
                "taskId": taskId}

    def saveNewValueByTaskId(self, newVal, taskId):
        self.taskRepo.saveDescription(newVal, taskId)
