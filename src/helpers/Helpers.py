from src.repos.ListRepo import ListRepo
from functools import wraps
from flask import redirect, session

listRepo = ListRepo()


def getHistoricalDataCacheKey(symbol):
    return "historical_statistics" + symbol


def getStatisticsDataCacheKey(symbol):
    return "get_statistics" + symbol


def login_required(f):
    """
    Decorate routes to require login.
    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def hasEmptyElements(itemList):
    for item in itemList:
        if len(item) < 1:
            return True
    return False


def hasMinElements(length, minimal):
    return length >= minimal


def isCategoryNameValid(name, userId, length, minList, minName):
    error = None
    if not hasMinElements(length, minList):
        error = "we need at least 1 item"
        return False, error
    if not hasMinElements(len(name), minName):
        error = "List of nothing?!?"
        return False, error

    if listRepo.hasActiveCategoryByName(name, userId):
        error = "you have such list already"
        return False, error

    return True, error


def isItemListValid(items):
    error = None
    if hasEmptyElements(items):
        error = "those input boxes are meant to be used"
        return False, error

    return True, error


def isListFound(items):
    error = None
    if not hasMinElements(len(items), listRepo.DEFAULT_MIN_ITEM_LENGTH):
        error = "list not found"
        return False, error

    return True, error


def isItemValid(item):
    error = None
    if not hasMinElements(len(item), listRepo.DEFAULT_MIN_STRING_LENGTH):
        error = "can't be empty"
        return False, error

    return True, error
