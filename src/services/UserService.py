from src.repos.UserRepo import UserRepo
from werkzeug.security import check_password_hash, generate_password_hash


class UserService:

    def __init__(self):
        self.userRepo = UserRepo()

    def getAllUsers(self):
        data = self.userRepo.getALlUsers()
        return data

    def registerNewUser(self, username, password, passwordRepeat):
        if not username:
            value = "you must provide username"
            return False, value
        if not password or not passwordRepeat:
            value = "you must provide password"
            return False, value
        if password != passwordRepeat:
            value = "passwords dont match"
            return False, value
        users = self.userRepo.getUserByUsername(username)
        if len(users) > 0:
            value = "think of another username"
            return False, value
        hashedPassword = generate_password_hash(password)
        self.userRepo.saveNewUser(username, hashedPassword)

        userItem = self.userRepo.getUserByUsername(username)[0]
        value = userItem["id"]

        return True, value

    def checkLoginCredentials(self, username, password):
        if not username:
            value = "username missing"
            return False, value
        if not password:
            value = "password missing"
            return False, value
        userCredentials = self.userRepo.getUserByUsername(username)
        if len(userCredentials) < 1:
            value = "username not found"
            return False, value
        if not check_password_hash(userCredentials[0]["hashed_pass"], password):
            value = "incorrect"
            return False, value
        value = userCredentials[0]["id"]

        return True, value

