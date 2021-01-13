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

    def checkLoginCredentials(self, username, password):
        if not username:
            value = "username missing"
            return False, value
        if not password:
            value = "password missing"
            return False, value
        userCredentials = self.databaseRepo.getUserByUsername(username)
        if len(userCredentials) < 1:
            value = "username not found"
            return False, value
        if not check_password_hash(userCredentials["hashed_pass"], password):
            value = "incorrect"
            return False, value
        value = userCredentials["id"]

        return True, value

