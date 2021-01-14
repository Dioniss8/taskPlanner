import http.client
from flask import session
from src.services.LoggingService import LoggingService


class BaseNbaService:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("api-nba-v1.rapidapi.com")
        self.loggingService = LoggingService()
        self.headers = {
            'x-rapidapi-key': "68a7808744msh45159e559d39863p1f1216jsn53dde588f2c0",
            'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
        }

    def getPlayersByLastName(self, lastName):
        url = "/players/lastname" + str(lastName)
        data = self.getAndFormatResponseAsString("GET", url)
        userId = session["user_id"]
        '''TODO'''
        return data

    def getAndFormatResponseAsString(self, requestType, url):

        self.conn.request(requestType, url, headers=self.headers)

        res = self.conn.getresponse()
        data = res.read().decode("utf8")

        return data
