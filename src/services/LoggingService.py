from src.repos.LogsRepo import LogsRepo
from flask import flash, redirect


class LoggingService:

    def __init__(self):
        self.logsRepo = LogsRepo()

    def saveGetAllUsersEvent(self, user_id):
        success, error = self.saveEventWithMessage("get_all_players_event", user_id)
        if not success:
            flash("GetAllUsers failed")
            return False, error

        return True, error

    def saveLoginEvent(self, userId):
        success, error = self.saveEventWithMessage("login_event", userId)
        if not success:
            flash("Login went wrong")
            return False, error

        return True, error

    def saveLogoutEvent(self, userId):
        success, error = self.saveEventWithMessage("logout_event", userId)

        if not success:
            flash("Something went wrong")
            return redirect('/')

        return True, error

    def saveEventWithMessage(self, eventType, userId, eventMessage=""):
        error = None
        if not userId:
            error = "Missing user id"
            return False, error
        logMessage = "User_" + str(userId) + eventMessage
        self.logsRepo.saveLogEvent(eventType, logMessage)

        return True, error
