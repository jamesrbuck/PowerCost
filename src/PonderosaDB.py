import mysql.connector
from mysql.connector.errors import Error

class PonderosaDB:
    def __init__(self,dbConfig):
        self.record_stmt = {}
        self.record_data = {}
        self.dbConfig = dbConfig

    def connect(self):
        try:
            self.conn = mysql.connector.connect(**self.dbConfig)
        except mysql.connector.Error as err:
            if self.conn.is_connected():
                self.conn.close()
            print(f"PonderosaDB.py: MySQL Error: {err}")
            raise

    def getConn(self):
        return self.conn

    def close(self):
        try:
            self.conn.close()
        except mysql.connector.Error as err:
            if self.conn.is_connected():
                self.conn.close()
            print(f"PonderosaDB.py: MySQL Error: {err}")
            raise

    def commit(self):
        try:
            self.conn.commit()
        except mysql.connector.Error as err:
            if self.conn.is_connected():
                self.conn.close()
            print(f"PonderosaDB.py: MySQL Error: {err}")
            raise

    def insert(self,myDate,myHour,mykWh):
        try:
            self.connect()
            self.record_stmt = ("INSERT INTO usage_e (UDate, UTime, kWh) VALUES (%(UDate)s, %(UTime)s, %(kWh)s)" )
            self.record_data = { 'UDate': myDate, 'UTime':myHour,  'kWh': mykWh }
            cursor = self.conn.cursor()
            cursor.execute(self.record_stmt,self.record_data)
            self.commit()
        except mysql.connector.Error as err:
            print(f"PonderosaDB.py: MySQL Error: {err}")
            raise
        finally:
            if self.conn.is_connected():
                cursor.close()
                self.close()

    def __str__(self):
        return(f"DB Userid   = {self.dbConfig['user']}, " +
             f"DB Host       = {self.dbConfig['host']}, " +
             f"DB Database   = {self.dbConfig['database']}")
