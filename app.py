from flask import Flask, render_template, request
from src.db import DataBase

app = Flask(__name__)


@app.route('/')
def hello_world():
    dataObj = DataBase()
    data = dataObj.getAllTasks()
    return render_template('index.html', data=data)


@app.route('/add', methods=["GET", "POST"])
def add_task():
    if request.method == "GET":
        return render_template('add.html')
    else:
        dataObj = DataBase()
        description = request.form.get("taskDescription")
        dataObj.setTask(description)
        data = dataObj.getAllTasks()
        return render_template('index.html', data=data)


if __name__ == '__main__':
    app.run()
