from flask import Flask, render_template, request, redirect
from src.db import DataBase
from src.helpers import hasEmptyElements

app = Flask(__name__)
app.debug = True

dataBaseObj = DataBase()


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
        return render_template('lists/index.html', lists=data)
    else:
        length = len(request.form)
        if length < 2:
            return redirect('/lists')
        name = request.form.get("category")
        if len(name) < 1:
            return redirect('/lists')
        items = []
        for i in range(length - 1):
            items.append(request.form.get(str(i)))
        if hasEmptyElements(items):
            return redirect('/lists')
        if dataBaseObj.hasActiveCategoryByName(name):
            return redirect('/lists')
        dataBaseObj.saveCategory(name, length - 1)
        category = dataBaseObj.getCategoryByName(name)[0]
        cat_id = category["id"]
        for item in items:
            dataBaseObj.saveItem(item, cat_id, True)
        return redirect('/lists')


@app.route('/lists/view', methods=["GET", "POST"])
def viewList():

    if request.method == "GET":
        categoryId = request.args.get("id")
        items = dataBaseObj.getListByCategoryId(categoryId)
        if len(items) < 1:
            return redirect('/lists')
        categoryName = items[0]["cat_name"]
        return render_template('lists/view.html',
                               categoryName=categoryName,
                               items=items,
                               categoryId=categoryId)


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
        if len(newItem) < 1:
            return redirect('/lists/view?id' + categoryId)
        dataBaseObj.saveItem(newItem, categoryId)
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
