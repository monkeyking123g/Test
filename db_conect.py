import os
import sqlite3



def conn_db():
    '''Conn DB'''
    app_path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(os.path.join(app_path, 'time_db.db'))
    return conn

  
def total_month_add(self, d, date_add, total):
    '''insert total in sqlite3
    '''
    insertQuery = """INSERT INTO  totale(datatime_add, total_ore) VALUES (?, ?);"""
    return d.execute(insertQuery, (date_add, total))
 