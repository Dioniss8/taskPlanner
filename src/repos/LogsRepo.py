from src.repos.BaseRepo import BaseRepo
from datetime import datetime


class LogsRepo(BaseRepo):

    def __init__(self):
        super().__init__()

    def getALlYahooFinanceEvents(self, eventType):
        '''should probably do only last 31 days here'''
        data = self.db.execute('''SELECT *
                                    FROM logs
                                    WHERE type=:eventType''',
                               eventType=eventType)
        return data

    def saveLogEvent(self, logType, logMessage):
        created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.db.execute('''INSERT INTO logs (type, message, created_at)
                            VALUES(:type , :message, :created_at)''',
                        type=logType, message=logMessage, created_at=created_at)

