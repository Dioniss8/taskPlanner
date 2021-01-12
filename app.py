import os

from flask import Flask, flash, render_template, request, redirect
from flask_session import Session
from src.Db import DataBase
from src.ListService import ListService
from src.TaskService import TaskService

app = Flask(__name__)

app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

dataBaseObj = DataBase()
ListService = ListService()
TaskService = TaskService()


@app.route('/')
def hello_world():
    data = TaskService.getAllTasks()
    return render_template('tasks/index.html', data=data)


@app.route('/login', methods=["GET", "POST"])
def login():

    if request.method == "GET":
        return render_template('login.html')


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "GET":

        return render_template('register.html')


@app.route('/add', methods=["GET", "POST"])
def add_task():
    if request.method == "GET":

        return render_template('tasks/add.html')
    else:
        description = request.form.get("taskDescription")
        data = TaskService.addTaskAndReturnAll(description)

        return render_template('tasks/index.html', data=data)


@app.route('/delete', methods=["GET"])
def delete():
    if request.method == "GET":
        taskId = int(request.args.get("id"))
        TaskService.deleteTaskById(taskId)

        return redirect('/')


@app.route('/edit', methods=["GET", "POST"])
def edit():

    if request.method == "GET":
        taskId = int(request.args.get("id"))
        data = TaskService.getPreviousTaskById(taskId)

        return render_template('tasks/edit.html',
                               previous=data["previous"],
                               taskId=data["taskId"])
    else:
        text = str(request.form.get("editedDesc"))
        taskId = int(request.form.get("id"))
        TaskService.saveNewValueByTaskId(text, taskId)

        return redirect('/')


@app.route('/lists', methods=["GET", "POST"])
def lists():

    if request.method == "GET":
        data = dataBaseObj.getAllCategories()
        return render_template('lists/index.html',
                               lists=data)
    else:
        length = len(request.form)
        name = request.form.get("category")
        items = []
        for i in range(length - 1):
            items.append(request.form.get(str(i)))
        success, error = ListService.saveList(name, length,
                                              dataBaseObj.DEFAULT_MIN_LIST_LENGTH,
                                              dataBaseObj.DEFAULT_MIN_STRING_LENGTH,
                                              items)
        if not success:
            flash(error)

        return redirect('/lists')


@app.route('/lists/view', methods=["GET", "POST"])
def viewList():

    if request.method == "GET":
        categoryId = request.args.get("id")
        success, value = ListService.viewListByCategoryId(categoryId)
        if not success:
            flash(value)
            return redirect('/lists')
        return render_template('lists/view.html',
                               categoryName=value["categoryName"],
                               items=value["items"],
                               categoryId=value["categoryId"])


@app.route('/lists/delete', methods=["GET"])
def deleteList():

    if request.method == "GET":
        categoryId = request.args.get("id")
        ListService.deleteListByCategoryId(categoryId)

        return redirect('/lists')


@app.route('/lists/view/add', methods=["POST"])
def addItemToList():

    if request.method == "POST":
        newItem = request.form.get("newItem")
        categoryId = request.form.get("categoryId")
        success, value = ListService.addItemToExistingList(newItem, categoryId)
        if not success:
            flash(value)

        return redirect('/lists/view?id=' + categoryId)


@app.route('/lists/view/delete', methods=["GET"])
def deleteItemInView():

    if request.method == "GET":
        itemId = int(request.args.get("id"))
        categoryId = request.args.get("cat_id")
        ListService.deleteItemAndAdjustCategory(itemId, categoryId)
        return redirect('/lists')


if __name__ == '__main__':
    app.run()
