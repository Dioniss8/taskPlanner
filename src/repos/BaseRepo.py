from cs50 import SQL


class BaseRepo:

    def __init__(self):
        self.db = SQL("sqlite:///identifier.sqlite")