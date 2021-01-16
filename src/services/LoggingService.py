from src.repos.LogsRepo import LogsRepo
from flask import flash, redirect

EVENT_YAHOO = "get_yahoo_event"
EVENT_GET_ALL_USERS = "get_all_players_event"
EVENT_GET_STATISTICS = "get_statistics_event"


class LoggingService:

    def __init__(self):
        self.logsRepo = LogsRepo()

    def saveGetStatisticsEvent(self, user_id):
        success, error = self.saveEventWithMessage(EVENT_YAHOO, user_id, EVENT_GET_STATISTICS)
        if not success:
            flash("GetStatistics event failed")
            return False, error

        return True, error

    def saveGetAllUsersEvent(self, user_id):
        success, error = self.saveEventWithMessage(EVENT_GET_ALL_USERS, user_id)
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
        logMessage = "User" + str(userId) + "," + eventMessage
        self.logsRepo.saveLogEvent(eventType, logMessage)

        return True, error

    def getAllYahooEvents(self):
        return self.logsRepo.getALlYahooFinanceEvents(EVENT_YAHOO)
