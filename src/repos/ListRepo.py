from src.repos.BaseRepo import BaseRepo

DEFAULT_DELETED = 0
DEFAULT_DONE = 0
DEFAULT_MIN_LIST_LENGTH = 2
DEFAULT_MIN_ITEM_LENGTH = 1
DEFAULT_MIN_STRING_LENGTH = 1


class ListRepo(BaseRepo):

    def __init__(self):
        super().__init__()
        self.DEFAULT_MIN_LIST_LENGTH = DEFAULT_MIN_LIST_LENGTH
        self.DEFAULT_MIN_STRING_LENGTH = DEFAULT_MIN_STRING_LENGTH
        self.DEFAULT_MIN_ITEM_LENGTH = DEFAULT_MIN_ITEM_LENGTH

    def addCategory(self, name, length):
        self.db.execute("""INSERT INTO categories (cat_name, len, deleted)
                            VALUES (:cat_name, :len, :deleted)""",
                        cat_name=name, len=length, deleted=DEFAULT_DELETED)

    def getCategoryByName(self, catName):
        category = self.db.execute("""SELECT *
                                        FROM categories
                                        WHERE cat_name=:cat_name
                                        AND deleted = 0""",
                                   cat_name=catName)
        return category

    def hasActiveCategoryByName(self, catName):
        categories = self.db.execute("""SELECT *
                                        FROM categories
                                        WHERE cat_name=:catName
                                        AND deleted = 0""",
                                     catName=catName)
        return len(categories) > 0

    def addLengthCategory(self, categoryId, opp=False):
        currentCount = self.db.execute("""SELECT *
                                            FROM categories
                                            WHERE id=:categoryId""",
                                       categoryId=categoryId)
        if opp:
            diff = -1
        else:
            diff = 1
        self.db.execute("""UPDATE categories
                            SET len=:newCount
                            WHERE id=:categoryId""",
                        newCount=currentCount[0]["len"] + diff,
                        categoryId=categoryId)

    def saveItem(self, itemName, cat_id, creation=False):
        if not creation:
            self.addLengthCategory(cat_id)
        self.db.execute("""INSERT INTO items (item_name, cat_id, deleted)
                            VALUES (:item_name, :cat_id, :deleted)""",
                        item_name=itemName, cat_id=cat_id, deleted=DEFAULT_DELETED)

    def getAllCategories(self):
        lists = self.db.execute("""SELECT *
                                    FROM categories
                                    WHERE deleted = 0""")
        return lists

    def getItemsByCategoryId(self, categoryId):
        items = self.db.execute("""SELECT *
                                    FROM items
                                    WHERE cat_id=:categoryId""",
                                categoryId=categoryId)
        return items

    def getListByCategoryId(self, categoryId):
        items = self.db.execute("""SELECT *, i.id as itemId
                                    FROM items as i
                                    JOIN categories as c on i.cat_id=c.id
                                    where c.id = :categoryId
                                    AND i.deleted = 0""",
                                categoryId=categoryId)
        return items

    def deleteCategoryById(self, categoryId):
        self.db.execute("""UPDATE categories
                            SET deleted = 1
                            WHERE id=:categoryId""",
                        categoryId=categoryId)

    def deleteItemById(self, itemId):
        self.db.execute("""UPDATE items
                            SET deleted = 1
                            WHERE id=:itemId""",
                        itemId=itemId)

    def deleteListByCategoryId(self, categoryId):
        items = self.getItemsByCategoryId(categoryId)
        for row in items:
            itemId = row["id"]
            self.deleteItemById(itemId)

        self.deleteCategoryById(categoryId)

