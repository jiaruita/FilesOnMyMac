import config
import sqlite3 as sqlite

def init_db():
    try:
        conn = sqlite.connect(config.dbconfig.name)
        cursor = conn.cursor()
        cursor.execute(config.create_tbl_files)
        cursor.execute(config.create_tbl_fs_structure)
        conn.commit()
        conn.close()
    except Exception as e:
        print "got exception in init_db()" + str(e)



def main():
    init_db()




