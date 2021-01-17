import http.client


class GeoDbService:

    def __init__(self):
        self.conn = http.client.HTTPSConnection("wft-geo-db.p.rapidapi.com")
        self.headers = {
            'x-rapidapi-key': "68a7808744msh45159e559d39863p1f1216jsn53dde588f2c0",
            'x-rapidapi-host': "wft-geo-db.p.rapidapi.com"
        }