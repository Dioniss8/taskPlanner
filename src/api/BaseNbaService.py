import http.client


class BaseNbaService:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("api-nba-v1.rapidapi.com")

        self.headers = {
            'x-rapidapi-key': "68a7808744msh45159e559d39863p1f1216jsn53dde588f2c0",
            'x-rapidapi-host': "api-nba-v1.p.rapidapi.com"
        }


