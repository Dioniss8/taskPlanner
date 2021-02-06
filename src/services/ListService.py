from src.repos.ListRepo import ListRepo
import src.helpers.Helpers as Helpers


class ListService:

    def __init__(self):
        self.listRepo = ListRepo()

    def getAllItemsByCategoryId(self, catId):
        return self.listRepo.getItemsByCategoryId(catId)

    def saveList(self, name, length, items, userId):
        success, error = Helpers.isCategoryNameValid(name, userId, length,
                                                     self.listRepo.DEFAULT_MIN_LIST_LENGTH,
                                                     self.listRepo.DEFAULT_MIN_STRING_LENGTH)
        if not success:
            return False, error

        success, error = Helpers.isItemListValid(items)
        if not success:
            return False, error

        self.listRepo.addCategory(name, length - 1, userId)
        category = self.listRepo.getCategoryByName(name, userId)[0]
        categoryId = category["id"]
        for item in items:
            self.listRepo.saveItem(item, categoryId, True)

        return True, error

    def viewListByCategoryId(self, categoryId):
        items = self.listRepo.getListByCategoryId(categoryId)
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

        self.listRepo.saveItem(newItem, categoryId)

        return True, error

    def getAllCategories(self, userId):

        return self.listRepo.getAllCategories(userId)

    def deleteListByCategoryId(self, categoryId):
        self.listRepo.deleteListByCategoryId(categoryId)

    def deleteItemAndAdjustCategory(self, itemId, categoryId):
        self.listRepo.deleteItemById(itemId)
        self.listRepo.addLengthCategory(categoryId, True)
