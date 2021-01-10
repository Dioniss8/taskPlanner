from flask import Flask, flash, render_template, request, redirect
from src.Db import DataBase
from src.ListService import ListService

app = Flask(__name__)
app.debug = True
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

dataBaseObj = DataBase()
ListService = ListService()


@app.route('/')
def hello_world():
    data = dataBaseObj.getAllTasks()
    return render_template('tasks/index.html', data=data)


@app.route('/add', methods=["GET", "POST"])
def add_task():
    if request.method == "GET":
        return render_template('tasks/add.html')
    else:
        description = request.form.get("taskDescription")
        dataBaseObj.setTask(description)
        data = dataBaseObj.getAllTasks()
        return render_template('tasks/index.html', data=data)


@app.route('/delete', methods=["GET"])
def delete():
    if request.method == "GET":
        taskId = int(request.args.get("id"))
        dataBaseObj.deleteTask(taskId)
        return redirect('/')


@app.route('/edit', methods=["GET", "POST"])
def edit():

    if request.method == "GET":
        taskId = int(request.args.get("id"))
        task = dataBaseObj.getTaskById(taskId)[0]
        previous = task["description"]
        return render_template('tasks/edit.html', previous=previous, taskId=taskId)
    else:
        text = str(request.form.get("editedDesc"))
        taskId = int(request.form.get("id"))
        dataBaseObj.saveDescription(text, taskId)
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
        dataBaseObj.deleteListByCategoryId(categoryId)
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
        dataBaseObj.deleteItemById(itemId)
        categoryId = request.args.get("cat_id")
        dataBaseObj.addLengthCategory(categoryId, True)
        return redirect('/lists')


if __name__ == '__main__':
    app.run()
