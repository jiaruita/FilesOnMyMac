__author__ = 'rujia'
import sqlite3 as sqlite
import config

dbconfig = config.dbconfig

class SqliteModel(object):
    def __init__(self):
        try:
            self.config = dbconfig
            self.conn = sqlite.connect(dbconfig['name'])
            self.conn.text_factory = str
        except Exception as e:
            print "got exception in SqliteModel init: " + str(e)
            exit(1)

    def _cursor(self):
        return self.conn.cursor()

    def insert_one_entry(self, sql, params):
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

    def insert_one_entry_get_id(self, sql, params):
        if not sql:
            return False
        try:
            # print sql, params
            cursor = self._cursor()
            cursor.execute(sql, params)
            self.conn.commit()
            result = cursor.lastrowid
            cursor.close()
            return result
        except Exception as err:
            print "exception in insert_one_entry_get_id(): " + str(err)
            return None

    def insert_many(self, sql, rows):
        # print "insert many: ", sql, rows
        if not sql:
            return False
        try:
            cursor = self._cursor()
            cursor.executemany(sql, rows)
            self.conn.commit()
            cursor.close()
            return True
        except Exception as err:
            print "exception in insert_many(): " + str(err)
            return False

    def select_all_rows(self, sql, params=None):
        if not sql:
            return False
        try:
            cursor = self._cursor()
            if params is None:
                cursor.execute(sql)
            else:
                cursor.execute(sql, params)
            # print sql
            rows = cursor.fetchall()
            cursor.close()
            return rows
        except Exception as e:
            print "got exception in select_all_rows(): ", str(e)
            return []
