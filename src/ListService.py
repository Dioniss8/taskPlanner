from src.Db import DataBase
import src.helpers as helpers


class ListService:

    def __init__(self):
        self.databaseRepo = DataBase()

    def saveList(self, name, length, minList, minName, items):
        success, error = helpers.isCategoryNameValid(name, length, minList, minName)
        if not success:
            return False, error

        success, error = helpers.isItemListValid(items)
        if not success:
            return False, error

        self.databaseRepo.addCategory(name, length - 1)
        category = self.databaseRepo.getCategoryByName(name)[0]
        categoryId = category["id"]
        for item in items:
            self.databaseRepo.saveItem(item, categoryId, True)

        return True, error

    def viewListByCategoryId(self, categoryId):
        items = self.databaseRepo.getListByCategoryId(categoryId)
        success, error = helpers.isListFound(items)
        if not success:
            return False, error

        categoryName = items[0]["cat_name"]
        data = {"categoryName": categoryName,
                "items": items,
                "categoryId": categoryId}

        return True, data

    def addItemToExistingList(self, newItem, categoryId):
        success, error = helpers.isItemValid(newItem)
        if not success:
            return False, error

        self.databaseRepo.saveItem(newItem, categoryId)

        return True, error


