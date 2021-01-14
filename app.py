from flask import Flask, flash, render_template, request, redirect, session
from flask_session import Session
from tempfile import mkdtemp
from src.services.ListService import ListService
from src.services.TaskService import TaskService
from src.services.UserService import UserService
from src.services.LoggingService import LoggingService
from src.helpers.Helpers import login_required

app = Flask(__name__)

app.debug = True

# This was needed for flashing messages from documentation
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

ListService = ListService()
TaskService = TaskService()
UserService = UserService()
LoggingService = LoggingService()


@app.route('/')
@login_required
def hello_world():
    userId = session["user_id"]
    data = TaskService.getAllTasks(userId)
    return render_template('tasks/index.html', data=data)


@app.route('/logout', methods=["GET"])
@login_required
def logout():
    if request.method == "GET":
        userId = session["user_id"]
        LoggingService.saveLogoutEvent(userId)

        session.clear()

        return redirect('/')


@app.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "GET":
        return render_template('login.html')

    else:
        success, value = UserService.checkLoginCredentials(
            request.form.get("username"),
            request.form.get("password"))

        if not success:
            flash(value)
            return redirect("/login")

        session["user_id"] = value

        LoggingService.saveLoginEvent(value)

        return redirect("/")


@app.route('/register', methods=["GET", "POST"])
def register():

    if request.method == "GET":
        return render_template('register.html')

    else:
        success, value = UserService.registerNewUser(
            request.form.get("username"),
            request.form.get("password0"),
            request.form.get("password1"))

        if not success:
            flash(value)
            return render_template('register.html')

        session["user_id"] = value

        return redirect('/')


@app.route('/add', methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "GET":

        return render_template('tasks/add.html')
    else:
        userId = session["user_id"]
        description = request.form.get("taskDescription")
        data = TaskService.addTaskAndReturnAll(description, userId)

        return render_template('tasks/index.html', data=data)


@app.route('/delete', methods=["GET"])
@login_required
def delete():
    if request.method == "GET":
        taskId = int(request.args.get("id"))
        TaskService.deleteTaskById(taskId)

        return redirect('/')


@app.route('/edit', methods=["GET", "POST"])
@login_required
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
@login_required
def lists():

    if request.method == "GET":
        data = ListService.getAllCategories()
        return render_template('lists/index.html',
                               lists=data)
    else:
        length = len(request.form)
        name = request.form.get("category")
        items = []
        for i in range(length - 1):
            items.append(request.form.get(str(i)))
        success, error = ListService.saveList(name, length, items)
        if not success:
            flash(error)

        return redirect('/lists')


@app.route('/lists/view', methods=["GET", "POST"])
@login_required
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
@login_required
def deleteList():

    if request.method == "GET":
        categoryId = request.args.get("id")
        ListService.deleteListByCategoryId(categoryId)

        return redirect('/lists')


@app.route('/lists/view/add', methods=["POST"])
@login_required
def addItemToList():

    if request.method == "POST":
        newItem = request.form.get("newItem")
        categoryId = request.form.get("categoryId")
        success, value = ListService.addItemToExistingList(newItem, categoryId)
        if not success:
            flash(value)

        return redirect('/lists/view?id=' + categoryId)


@app.route('/lists/view/delete', methods=["GET"])
@login_required
def deleteItemInView():

    if request.method == "GET":
        itemId = int(request.args.get("id"))
        categoryId = request.args.get("cat_id")
        ListService.deleteItemAndAdjustCategory(itemId, categoryId)
        return redirect('/lists')


@app.route('/nba')
def index():
    return render_template('nba/index.html')
    '''@login_required'''


if __name__ == '__main__':
    app.run()
