__author__ = 'rujia'
import sqlite3 as sqlite
import config

dbconfig = config.dbconfig

class SqliteModel(object):
    def __init__(self):
        try:
            self.config = dbconfig
            self.conn = sqlite.connect(dbconfig['name'])
        except Exception as e:
            print "got exception in SqliteModel init: " + str(e)
            exit(1)

    def _cursor(self):
        return self.conn.cursor()

    def insert_one_entry(self, sql, *params):
        if not sql:
            return False
        try:
            cursor = self._cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            cursor.close()
            return True
        except Exception as e:
            print "got exception in insert_one_entry(): ", str(e)
            return False

    def select_all_rows(self, sql, *params):
        if not sql:
            return False
        try:
            cursor = self._cursor()
            cursor.execute(sql, params)
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print "got exception in select_all_rows(): ", str(e)
            return []
