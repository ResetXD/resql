from typing import Any
import sqlite3
import re
from resql.core.errors import PydbInvalidTableName

regex = re.compile("[A-z0-9]+")

class ReSql:
    default_row:str = "DEFAULT_RESQL_TABLE"

    def __init__(self, path:str=":memory:", props:dict={}):
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS DEFAULT_RESQL_TABLE (ID TEXT, value TEXT)")

    def commit(self):
        self.connection.commit()
        return 

    def insert(self,key:str,value:Any, table:str=default_row):
        self.cursor
        self.cursor.execute(f"INSERT INTO {table} (ID, value) VALUES (?, ?)", (key, value))
        self.commit()
        return {"status":"success"}

    def find(self,key:str, table:str=default_row):
        self.cursor.execute(f"SELECT * FROM {table} WHERE ID = ?", (key,))
        resp = self.cursor.fetchone()
        self.commit()
        return resp[1] if resp != None else None

    def get(self,key:str, table:str=default_row):
        self.cursor.execute(f"SELECT * FROM {table} WHERE ID = ?", (key,))
        resp = self.cursor.fetchone()
        self.commit()
        return resp[1] if resp != None else None

    def all(self, table:str=default_row):
        self.cursor.execute(f"SELECT * FROM {table}")
        resp = self.cursor.fetchall()
        self.commit()
        return resp if resp != None else None

    def wipe(self, table:str=default_row):
        self.cursor.execute(f"delete from {table}")
        self.commit()
        return {"status":"success"}

    def delete(self,key:str, table:str=default_row):
        self.cursor = self.connection.cursor()
        self.cursor.execute(f"DELETE FROM {table} WHERE ID = ?", (key,))
        self.commit()
        return {"status":"success"}

    def create_table(self,name:str):
        if regex.match(name) != None and regex.match(name)[0] == name:
            self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {name} (ID TEXT, value TEXT)")
        else:
            raise PydbInvalidTableName("Invalid table name")
        self.commit()
        return {"status":"success","table":name}

    def run(self,sql:str):
        self.cursor.execute(sql)
        self.commit()
    
    def db_cursor(self):
        return self.cursor
