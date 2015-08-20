import os
import db_model
import traceback

db = db_model.SqliteModel()

insert_one_file = (
    "INSERT INTO tbl_files "
    "(name, abspath, size, filesize, isdir) "
    "VALUES "
    "(?, ?, ?, ?, ?)"
)

insert_one_child = (
    "INSERT INTO tbl_fs_structure "
    "(parent, child) "
    "VALUES "
    "(?, ?)"
)

update_size = (
    "UPDATE tbl_files "
    "SET size=?, filesize=? "
    "WHERE id=?"
)

update_file_size = (
    "UPDATE tbl_files "
    "SET filesize=? "
    "WHERE id=?"
)

update_total_size = (
    "UPDATE tbl_files "
    "SET size=? "
    "WHERE id=?"
)

get_dir_total_sizes = (
    "SELECT parent, SUM(f.size) "
    "FROM tbl_fs_structure AS s "
    "INNER JOIN tbl_files AS f "
    "ON s.child=f.id "
    "GROUP BY parent"
)

get_dir_file_sizes = (
    "SELECT parent, SUM(f.filesize) "
    "FROM tbl_fs_structure AS s "
    "INNER JOIN tbl_files AS f "
    "ON s.child=f.id "
    "WHERE f.isdir=0 "
    "GROUP BY parent"
)

class FSNode(object):
    def __init__(self, name=None, abs_path=None,
                 size=None, files_size=None, is_dir=True):
        self.abs_path = abs_path
        if name is None:
            path, tail = os.path.split(abs_path)
            self.name = path if tail == "" else tail
        else:
            self.name = name
        self.size = 0 if size is None else size
        self.files_size = 0 if files_size is None else files_size
        self.children = []
        self.is_dir = is_dir
        # insert the entry and get the auto-increment id for this file
        rowid = db.insert_one_entry_get_id(
            insert_one_file,
            (self.name, self.abs_path, self.size, self.files_size, self.is_dir)
        )
        if rowid is not None:
            self.rowid = rowid
        else:
            print "fail to insert new entry for " + str(self)

    def __lt__(self, other):
        return self.size < other.size

    def __eq__(self, other):
        return self.size == other.size

    def __str__(self):
        return 'Name: {0}\tPath: {1}\tSize: {2}'.format(self.name,
                                                        self.abs_path,
                                                        self.size)

    def __repr__(self):
        return 'Name: {0}\tPath: {1}\tSize: {2}'.format(self.name,
                                                        self.abs_path,
                                                        self.size)

    def get_children(self):
        """
        Get the list of children directories or files under a directory.
        Update the children attribute for self, and return the results.
        :return
            a list of FSNode objects
        """
        try:
            if not os.path.isdir(self.abs_path):
                self.is_dir = False
                return []
            children = []
            for name in os.listdir(self.abs_path):
                child_abs_path = os.path.join(self.abs_path, name)
                if os.path.isdir(child_abs_path):
                    # the child is a directory
                    children.append(FSNode(name, child_abs_path))
                else:
                    # the child is a file
                    s = os.path.getsize(child_abs_path)
                    children.append(FSNode(name=name,
                                           abs_path=child_abs_path,
                                           size=s,
                                           files_size=s,
                                           is_dir=False))
            self.children = children
            rows = []
            for child in children:
                rows.append(
                    (self.rowid, child.rowid)
                )
            # update parent-child relationship
            db.insert_many(insert_one_child, rows)
            return children
        except Exception as e:
            #print "exception in get_children(): ", str(e)
            print "trackback: " + str(traceback.format_exc())
            return []

    def update_size(self):
        """
        Update size info for one entry.
        Not used.
        """
        db.insert_one_entry(
            update_size, (self.size, self.files_size, self.rowid)
        )


class DirObj(FSNode):
    pass

def traverse(start):
    """
    Traverse through the file system starting from "start".
    During the traversal, entries of files or directories are inserted,
    and parent-child relationship will be created and inserted.
    """
    if start is None:
        return None
    if not isinstance(start, FSNode):
        return None
    stack = [start]
    while stack:
        next_node = stack.pop()
        # print "next: ", str(next_node)
        children = next_node.get_children()
        # print "children: ", str(children)
        for child in children:
            stack.append(child)

def calc_size(start_node):
    """
    Calculate the size for files or directories starting from one node.
    """
    if not start_node or not isinstance(start_node, FSNode):
        return None
    rows = db.select_all_rows(get_dir_file_sizes)
    for row in rows:
        db.insert_one_entry(update_file_size, (row[1], row[0]))

    # rows = db.select_all_rows(get_dir_total_sizes)
    # for row in rows:
    #     db.insert_one_entry(update_total_size, (row[1], row[0]))



class FSTree(object):
    def __init__(self, root=None):
        self.root = root

    def traverse(self, start=None):
        if start is None:
            start = self.root
        if not isinstance(start, FSNode):
            raise Exception(str(start) + " is not a FSNode")
        children_names = start.get_children()
        for child in children_names:
            start.children.append(FSNode(child))


if __name__ == "__main__":
    root = FSNode(abs_path="/Users/rujia/python")
    traverse(root)
    calc_size(root)

