from cs50 import SQL
from datetime import datetime

DEFAULT_DONE = 0
DEFAULT_DELETED = 0


class DataBase:

    DEFAULT_MIN_LIST_LENGTH = 2
    DEFAULT_MIN_ITEM_LENGTH = 1
    DEFAULT_MIN_STRING_LENGTH = 1

    def __init__(self):
        self.db = SQL("sqlite:///tasks.db")

    def getAllTasks(self):
        tasks = self.db.execute("SELECT * FROM tasks WHERE deleted = 0")

        return tasks

    def setTask(self, description):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute("""INSERT INTO tasks (description, done, deleted, created_at)
                            VALUES (:description, :done, :deleted, :created_at)""",
                        description=description, done=DEFAULT_DONE,
                        deleted=DEFAULT_DELETED, created_at=created_at)

    def deleteTask(self, taskId):
        self.db.execute("""UPDATE tasks
                            SET deleted = 1
                            WHERE id=:taskId""", taskId=taskId)

    def getTaskById(self, taskId):
        tasks = self.db.execute("""SELECT *
                            FROM tasks
                            WHERE id=:taskId""", taskId=taskId)
        return tasks

    def saveDescription(self, text, taskId):
        self.db.execute("""UPDATE tasks
                            SET description = :text
                            WHERE id=:taskId""",
                        text=text, taskId=taskId)

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

    def saveNewUser(self, username, hashedPassword):
        self.db.execute("""INSERT INTO users (username, hashed_pass)
                            VALUES (:username, :hashedPassword)""",
                        username=username, hashedPassword=hashedPassword)

    def getUserByUsername(self, username):
        users = self.db.execute("""SELECT *
                                    FROM users
                                    WHERE username=:username""",
                                username=username)
        return users
