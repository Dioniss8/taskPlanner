def hasEmptyElements(itemList):
    for item in itemList:
        if len(item) < 1:
            return True
    return False

