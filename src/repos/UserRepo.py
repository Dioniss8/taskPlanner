from src.repos.BaseRepo import BaseRepo


class UserRepo(BaseRepo):

    def __init__(self):
        super().__init__()

    def getALlUsers(self):
        users = self.db.execute('''SELECT *
                                    FROM users''');
        return users

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
