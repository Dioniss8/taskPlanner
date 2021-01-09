from flask import Flask, render_template, request, redirect
from src.db import DataBase

app = Flask(__name__)
app.debug = True

dataBaseObj = DataBase()


@app.route('/')
def hello_world():
    data = dataBaseObj.getAllTasks()
    return render_template('index.html', data=data)


@app.route('/add', methods=["GET", "POST"])
def add_task():
    if request.method == "GET":

        return render_template('add.html')
    else:
        description = request.form.get("taskDescription")
        dataBaseObj.setTask(description)
        data = dataBaseObj.getAllTasks()

        return render_template('index.html', data=data)


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

        return render_template('edit.html', previous=previous, taskId=taskId)
    else:
        text = str(request.form.get("editedDesc"))
        taskId = int(request.form.get("id"))
        dataBaseObj.saveDescription(text, taskId)

        return redirect('/')


@app.route('/lists', methods=["GET", "POST"])
def lists():

    if request.method == "GET":
        data = dataBaseObj.getAllLists()

        return render_template('lists.html', lists=data)
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

        before = len(dataBaseObj.getCategoryByName(name))
        if before > 0:

            return redirect('/lists')

        dataBaseObj.saveCategory(name, length - 1)
        category = dataBaseObj.getCategoryByName(name)[0]
        cat_id = category["id"]
        for item in items:
            dataBaseObj.saveItem(item, cat_id)

        return redirect('/')


if __name__ == '__main__':
    app.run()
