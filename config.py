__author__ = 'rujia'

dbconfig = {
    "name": "fsinfo.db"
}


create_tbl_files = (
    "CREATE TABLE IF NOT EXISTS tbl_files ("
    "id INTEGER PRIMARY KEY AUTOINCREMENT, "
    "name VARCHAR NOT NULL,"
    "abspath VARCHAR NOT NULL, "
    "size INTEGER, "
    "isdir INTEGER "
    ");"
)

create_tbl_fs_structure = (
    "CREATE TABLE IF NOT EXISTS tbl_fs_structure ("
    "parent INTEGER NOT NULL, "
    "child INTEGER NOT NULL, "
    "PRIMARY KEY (parent, child)"
    ");"
)