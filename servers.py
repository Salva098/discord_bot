import sqlite3

class Servers():
    def __init__(self):
        self.conn=sqlite3.connect("bot.bd",check_same_thread=False)
        