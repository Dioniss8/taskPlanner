from src.repos.LogsRepo import LogsRepo
from flask import flash, redirect

'''Should fix the flash messages, but pretty sure this doesnt work,
do I even need to error check log messages???
!!! This doesnt really makes sense to make this as... 
'''

EVENT_YAHOO = "get_yahoo_event"
EVENT_GET_ALL_USERS = "get_all_players_event"
EVENT_GET_STATISTICS = "get_statistics_event"
EVENT_GET_HISTORICAL_DATA = "get_historical_data_event"
EVENT_REGISTER = "register_event"


class LoggingService:

    def __init__(self):
        self.logsRepo = LogsRepo()

    def saveGetHistoricalDataEvent(self, user_id):
        success, error = self.saveEventWithMessage(EVENT_YAHOO, user_id, EVENT_GET_HISTORICAL_DATA)
        if not success:
            flash("GetHistory event failed")
            return False, error

        return True, error

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

    def saveRegisterEvent(self, userId):
        eventMessage = "userHasRegistered"
        success, error = self.saveEventWithMessage(EVENT_REGISTER, userId, eventMessage)
        if not success:
            flash("Register event failed")
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
        logMessage = "user_id:" + str(userId)
        if len(eventMessage) > 0:
            logMessage += ",message:" + str(eventMessage)
        self.logsRepo.saveLogEvent(eventType, logMessage)

        return True, error

    def getAllYahooEvents(self):
        return self.logsRepo.getALlYahooFinanceEvents(EVENT_YAHOO)
