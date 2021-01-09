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


@app.route('/lists', methods=["GET"])
def lists():

    if request.method == "GET":

        return render_template('index-lists.html')


if __name__ == '__main__':
    app.run()
