import http.client

DEFAULT_REGION = "US"


class BaseYahooFinanceService:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("apidojo-yahoo-finance-v1.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': "68a7808744msh45159e559d39863p1f1216jsn53dde588f2c0",
            'x-rapidapi-host': "apidojo-yahoo-finance-v1.p.rapidapi.com"
        }

    def getStatisticsBySymbolName(self, symbolName):
        url = "/stock/v2/get-statistics?symbol=" + symbolName + "&region=" + DEFAULT_REGION

        data = self.getAndFormatResponseAsString("GET", url)
        return data

    def getAndFormatResponseAsString(self, requestType, url):

        self.conn.request(requestType, url, headers=self.headers)

        res = self.conn.getresponse()
        data = res.read().decode("utf8")

        return data
