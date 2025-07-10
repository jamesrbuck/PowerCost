"""
Test database configuration
"""
from time import time
from powercost_project import DatabaseConfig


dbConfig  = {'user': 'U', 'password': 'P',
             'host': 'localhost', 'database': 'pse',
             'raise_on_warnings': True}

mytime    = time.localtime()
myDate    = time.strftime('%Y-%m-%d', mytime)
myHour    = time.strftime('%H:%M:%S', mytime)
MYKWH     = 3.65

#myDate = 'XXX'  # Bad date as test for the exception

db = DatabaseConfig(dbConfig)
db.insert(myDate, myHour, MYKWH)
print(db)
