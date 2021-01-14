from src.Db import UserRepo
import src.Helpers as Helpers


class ListService:

    def __init__(self):
        self.databaseRepo = UserRepo()

    def saveList(self, name, length, items):
        success, error = Helpers.isCategoryNameValid(name, length,
                                                     self.databaseRepo.DEFAULT_MIN_LIST_LENGTH,
                                                     self.databaseRepo.DEFAULT_MIN_STRING_LENGTH)
        if not success:
            return False, error

        success, error = Helpers.isItemListValid(items)
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
        success, error = Helpers.isListFound(items)
        if not success:
            return False, error

        categoryName = items[0]["cat_name"]
        data = {"categoryName": categoryName,
                "items": items,
                "categoryId": categoryId}

        return True, data

    def addItemToExistingList(self, newItem, categoryId):
        success, error = Helpers.isItemValid(newItem)
        if not success:
            return False, error

        self.databaseRepo.saveItem(newItem, categoryId)

        return True, error

    def getAllCategories(self):

        return self.databaseRepo.getAllCategories()

    def deleteListByCategoryId(self, categoryId):
        self.databaseRepo.deleteListByCategoryId(categoryId)

    def deleteItemAndAdjustCategory(self, itemId, categoryId):
        self.databaseRepo.deleteItemById(itemId)
        self.databaseRepo.addLengthCategory(categoryId, True)
