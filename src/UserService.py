from src.Db import DataBase
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:

    def __init__(self):
        self.databaseRepo = DataBase()

    def registerNewUser(self, username, password, passwordRepeat):
        error = None
        if not username:
            error = "you must provide username"
            return False, error
        if not password or not passwordRepeat:
            error = "you must provide password"
            return False, error
        if password != passwordRepeat:
            error = "passwords dont match"
            return False, error
        users = self.databaseRepo.getUserByUsername(username)
        if len(users) > 0:
            error = "think of another username"
            return False, error

        hashedPassword = generate_password_hash(password)
        self.databaseRepo.saveNewUser(username, hashedPassword)

        return True, error



