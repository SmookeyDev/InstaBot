import time
import redis
import sqlite3
from threading import Lock

lock = Lock()

def decode_bytes_dict(temp):
    return {x.decode():temp[x].decode() for x in temp}

class Sql:
    def __init__(self):
        try:
            lock.acquire(True)
            self.conn = sqlite3.connect("data.db", check_same_thread = False)
            self.conne = self.conn.cursor()
            self.conn.execute('''CREATE TABLE IF NOT EXISTS SETTINGS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
            NAME           TEXT    NOT NULL,
            VALUE           TEXT    NOT NULL);''')
            self.conn.execute('''CREATE TABLE IF NOT EXISTS CUSERS
            (ID INTEGER PRIMARY KEY AUTOINCREMENT     NOT NULL,
            NAME           TEXT    NOT NULL,
            VALUE           TEXT    NOT NULL);''')
        finally:
            lock.release()

    def set(self, name, value):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM SETTINGS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                self.conn.execute("UPDATE SETTINGS SET NAME = ?, VALUE = ? WHERE NAME = ?", [name, value, name])
                self.conn.commit()
                return "updated"
            else:
                self.conn.execute('INSERT INTO SETTINGS (ID, NAME, VALUE) VALUES (NULL, ?, ?)', [name, value])
                self.conn.commit()
                return "registered"
        finally:
            lock.release()

    def get(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM SETTINGS WHERE NAME = ?", [name])
            for i in self.conne.fetchall():
                return i[2]
        finally:
            lock.release()

    def exists(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM SETTINGS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                return True
            else:
                return False
        finally:
            lock.release()
    def delete(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM SETTINGS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                self.conne.execute("DELETE FROM SETTINGS WHERE NAME = ?", [name])
                self.conn.commit()
                return 'OK'
            else:
                return False
        finally:
            lock.release()

    def cset(self, name, value):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM CUSERS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                self.conn.execute("UPDATE CUSERS SET NAME = ?, VALUE = ? WHERE NAME = ?", [name, value, name])
                self.conn.commit()
                return "updated"
            else:
                self.conn.execute('INSERT INTO CUSERS (ID, NAME, VALUE) VALUES (NULL, ?, ?)', [name, value])
                self.conn.commit()
                return "registered"
        finally:
            lock.release()

    def cget(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM CUSERS WHERE NAME = ?", [name])
            for i in self.conne.fetchall():
                return i[2]
        finally:
            lock.release()

    def cexists(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM CUSERS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                return True
            else:
                return False
        finally:
            lock.release()

    def cdelete(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM CUSERS WHERE NAME = ?", [name])
            if self.conne.fetchone() is not None:
                self.conne.execute("DELETE FROM CUSERS WHERE NAME = ?", [name])
                self.conn.commit()
                return 'OK'
            else:
                return False
        finally:
            lock.release()

    def hset(self, name, value, key):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM HUSERS WHERE VALUE = ?", [value])
            if self.conne.fetchone() is not None:
                self.conn.execute("UPDATE HUSERS SET NAME = ?, VALUE = ?, KEY = ? WHERE value = ?", [name, value, key, value])
                self.conn.commit()
                return "updated"
            else:
                self.conn.execute('INSERT INTO HUSERS (ID, NAME, VALUE, KEY) VALUES (NULL, ?, ?, ?)', [name, value, key])
                self.conn.commit()
                return "registered"
        finally:
            lock.release()

    def hget(self, name, value):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM HUSERS WHERE NAME = ? AND VALUE = ?", [name, value])
            for i in self.conne.fetchall():
                return i[3]
        finally:
            lock.release()

    def hgetall(self, name):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM HUSERS WHERE NAME = ?", [name])
            getall = {}
            for i in self.conne.fetchall():
                getall[i[2]]= i[3]
                return getall
        finally:
            lock.release()

    def hdelete(self, value):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM HUSERS WHERE VALUE = ?", [value])
            if self.conne.fetchone() is not None:
                self.conne.execute("DELETE FROM HUSERS WHERE VALUE = ?", [value])
                self.conn.commit()
                return 'OK'
            else:
                return False
        finally:
            lock.release()

    def hexists(self, name, value):
        try:
            lock.acquire(True)
            self.conne.execute("SELECT * FROM CUSERS WHERE NAME = ? AND VALUE", [name, value])
            if self.conne.fetchone() is not None:
                return True
            else:
                return False
        finally:
            lock.release()
