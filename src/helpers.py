from src.Db import DataBase

databaseObj = DataBase()


def hasEmptyElements(itemList):
    for item in itemList:
        if len(item) < 1:
            return True
    return False


def hasMinElements(length, minimal):
    return length >= minimal


def isCategoryNameValid(name, length, minList, minName):
    error = None
    if not hasMinElements(length, minList):
        error = "we need at least 1 item"
        return False, error
    if not hasMinElements(len(name), minName):
        error = "List of nothing?!?"
        return False, error

    if databaseObj.hasActiveCategoryByName(name):
        error = "you have such list already"
        return False, error

    return True, error


def isItemListValid(items):
    error = None
    if hasEmptyElements(items):
        error = "those input boxes are meant to be used"
        return False, error

    return True, error
