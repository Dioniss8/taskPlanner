from flask import Flask, flash, json, render_template, request, redirect, session
from flask_session import Session
from flask_caching import Cache
from tempfile import mkdtemp
from src.services.ListService import ListService
from src.services.TaskService import TaskService
from src.services.UserService import UserService
from src.services.LoggingService import LoggingService
from src.api.BaseYahooFinanceService import BaseYahooFinanceService
from src.api.GetStatisticsMapper import *
from src.helpers.Helpers import login_required, getHistoricalDataCacheKey, getStatisticsDataCacheKey

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

# Configure cache
app.config["CACHE_TYPE"] = "simple"
app.config["CACHE_DEFAULT_TIMEOUT"] = 300

Session(app)
cache = Cache(app)


BaseYahooFinanceService = BaseYahooFinanceService()
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


@app.route('/multiples')
@login_required
def multiples():
    userId = session["user_id"]
    categories = ListService.getAllCategories(userId)
    return render_template('multiples/index.html', categories=categories)


@app.route('/api/multiples/get-data/', methods=["POST"])
@login_required
def apiGetData():
    if request.method == "POST":
        groups = request.form.getlist("groups-chosen")

        store = []
        for group in groups:
            categoryItems = ListService.getAllItemsByCategoryId(int(group))
            for item in categoryItems:
                stockData = {}
                symbolName = item["item_name"]

                cachedValue = cache.get(getStatisticsDataCacheKey(symbolName))
                if not cachedValue:
                    success, data = BaseYahooFinanceService.getStatisticsBySymbolName(symbolName)
                    cache.set(getStatisticsDataCacheKey(symbolName), [success, data])
                    userId = session["user_id"]
                    LoggingService.saveGetStatisticsEvent(userId)
                else:
                    success, data = cachedValue[0], cachedValue[1]

                if not success:
                    flash(data)
                    return redirect('/multiples')

                response = json.loads(data)

                stockData["symbol"] = response["symbol"]

                financialData = response["financialData"]
                for category in FINANCIAL_STATISTICS_CATEGORIES:
                    stockData[category] = financialData[category]

                defaultKeyStatistics = response["defaultKeyStatistics"]
                for category in DEFAULT_KEY_STATISTICS_CATEGORIES:
                    stockData[category] = defaultKeyStatistics[category]

                summaryDetail = response["summaryDetail"]
                for category in SUMMARY_DETAIL_CATEGORIES:
                    stockData[category] = summaryDetail[category]

                store.append(stockData)

        return json.jsonify({
            'success': True,
            'data': store,
        })


@app.route('/multiples/get-data', methods=["POST"])
@login_required
def getData():
    if request.method == "POST":
        groups = request.form.getlist("groups-chosen")

        store = []
        for group in groups:
            categoryItems = ListService.getAllItemsByCategoryId(int(group))
            for item in categoryItems:
                stockData = {}
                symbolName = item["item_name"]

                cachedValue = cache.get(getStatisticsDataCacheKey(symbolName))
                if not cachedValue:
                    success, data = BaseYahooFinanceService.getStatisticsBySymbolName(symbolName)
                    cache.set(getStatisticsDataCacheKey(symbolName), [success, data])
                    userId = session["user_id"]
                    LoggingService.saveGetStatisticsEvent(userId)
                else:
                    success, data = cachedValue[0], cachedValue[1]

                if not success:
                    flash(data)
                    return redirect('/multiples')

                response = json.loads(data)

                stockData["symbol"] = response["symbol"]

                financialData = response["financialData"]
                for category in FINANCIAL_STATISTICS_CATEGORIES:
                    stockData[category] = financialData[category]

                defaultKeyStatistics = response["defaultKeyStatistics"]
                for category in DEFAULT_KEY_STATISTICS_CATEGORIES:
                    stockData[category] = defaultKeyStatistics[category]

                summaryDetail = response["summaryDetail"]
                for category in SUMMARY_DETAIL_CATEGORIES:
                    stockData[category] = summaryDetail[category]

                store.append(stockData)

        keys = store[0].keys()
        keyNames = []
        for key in keys:
            keyNames.append(CATEGORY_NAME_MAPPER[key])

        return render_template('multiples/analyze.html',
                               data=store, keys=keys, keyNames=keyNames)

    else:

        return redirect('/multiples')


@app.route('/api/get-historical-data/', methods=["POST"])
@login_required
def historicalData():
    usageYahooTotal = len(LoggingService.getAllYahooEvents())
    symbol = request.form.get("symbol")
    if len(symbol) < 1:
        return json.jsonify({
            'success': False,
            'reason': 'missing search key',
            'usage': usageYahooTotal,
        })

    cachedValue = cache.get(getHistoricalDataCacheKey(symbol))
    if not cachedValue:
        success, data = BaseYahooFinanceService.getHistoricalDataBySymbol(symbol)
        cache.set(getHistoricalDataCacheKey(symbol), [success, data])
        user_id = session["user_id"]
        LoggingService.saveGetHistoricalDataEvent(user_id)
    else:
        success, data = cachedValue[0], cachedValue[1]

    usageYahooTotal = len(LoggingService.getAllYahooEvents())
    if data.find('empty response') > -1:
        return json.jsonify({
            'success': False,
            'reason': 'symbol not found',
            'usage': usageYahooTotal,
        })

    response = json.loads(data)

    usageYahooTotal = len(LoggingService.getAllYahooEvents())
    return json.jsonify({
        'success': True,
        'timePoints': len(response["prices"]),
        'data': response["prices"],
        'usage': usageYahooTotal,
    })


@app.route('/api/get-statistics/', methods=["POST"])
@login_required
def getStatistics():
    if request.method == "POST":
        usageYahooTotal = len(LoggingService.getAllYahooEvents())
        symbol = request.form.get("symbol")
        if len(symbol) < 1:
            return json.jsonify({
                'success': False,
                'reason': 'missing search key',
                'usage': usageYahooTotal,
            })

        cachedValue = cache.get(getStatisticsDataCacheKey(symbol))
        if not cachedValue:
            success, data = BaseYahooFinanceService.getStatisticsBySymbolName(symbol)
            cache.set(getStatisticsDataCacheKey(symbol), [success, data])
            user_id = session["user_id"]
            LoggingService.saveGetStatisticsEvent(user_id)
        else:
            success, data = cachedValue[0], cachedValue[1]

        usageYahooTotal = len(LoggingService.getAllYahooEvents())
        if data.find('empty response') > -1:
            return json.jsonify({
                'success': False,
                'reason': 'symbol not found',
                'usage': usageYahooTotal,
            })

        response = json.loads(data)

        symbol = response["symbol"]

        quoteType = response["quoteType"]
        '''This should be used in the view'''
        exchange = quoteType["exchange"]
        longName = quoteType["longName"]

        financialStatistics = response["financialData"]
        defaultKeyStats = response["defaultKeyStatistics"]
        summaryDetail = response["summaryDetail"]

        usageYahooTotal = len(LoggingService.getAllYahooEvents())
        return json.jsonify(({
            'financialStatistics': financialStatistics,
            'defaultKeyStatistics': defaultKeyStats,
            'summaryDetail': summaryDetail,
            'longName': longName,
            'success': int(success),
            'symbol': symbol,
            'usage': usageYahooTotal,
        }))


@app.route('/api/get-all-users/')
@login_required
def getAllUsers():
    user_id = session["user_id"]
    LoggingService.saveGetAllUsersEvent(user_id)
    data = UserService.getAllUsers()
    return json.jsonify({
        'data': data
    })


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
        LoggingService.saveRegisterEvent(value)

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
        userId = session["user_id"]
        data = ListService.getAllCategories(userId)
        return render_template('lists/index.html',
                               lists=data)
    else:
        userId = session["user_id"]
        length = len(request.form)
        name = request.form.get("category")
        items = []
        for i in range(length - 1):
            items.append(request.form.get(str(i)))
        success, error = ListService.saveList(name, length, items, userId)
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


@app.route('/apis')
@login_required
def index():
    usageYahoo = len(LoggingService.getAllYahooEvents())
    return render_template('apis/index.html', usageYahoo=usageYahoo)


if __name__ == '__main__':
    app.run()
