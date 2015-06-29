import os
import heapq
from collections import deque

class FSNode(object):
    def __init__(self, name=None, abs_path=None, size=None, is_dir=True):
        self.abs_path = abs_path
        if name is None:
            path, tail = os.path.split(abs_path)
            if tail == "":
                self.name = path
            else:
                self.name = tail
        else:
            self.name = name
        self.size = 0 if size is None else size
        self.children = []
        self.is_dir = is_dir

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
                    children.append(FSNode(name, child_abs_path))
                else:
                    children.append(FSNode(name=name,
                                           abs_path=child_abs_path,
                                           size=os.path.getsize(child_abs_path),
                                           is_dir=False))
            self.children = children
            return children
        except Exception as e:
            print "exception in get_children(): ", str(e)


class DirObj(FSNode):
    pass


def calc_size_in_traversal(start):
    if start is None:
        return None
    if not isinstance(start, FSNode):
        return None
    if not start.is_dir:
        return start.size
    children = start.get_children()
    total_size = 0
    for child in children:
        this_size = calc_size_in_traversal(child)
        if this_size is not None:
            total_size += this_size
    return total_size


def traverse(start):
    if start is None:
        return None
    if not isinstance(start, FSNode):
        return None
    stack = [start]
    while stack:
        next_node = stack.pop()
        print "next: ", str(next_node)
        children = next_node.get_children()
        print "children: ", str(children)
        for child in children:
            stack.append(child)



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



def get_entry_names_in_dir(path):
    """
    Get the list of entry names under a directory.
    :return
        a list of strings
    """
    if not os.path.isdir(path):
        raise Exception(str(path) + ' should be a dir')
    return os.listdir(path)
        

def sort_all():
    files = []
    errors = []
    for path, subdirs, subfiles in os.walk('/'):
        for subfile in subfiles:
            subfile = os.path.join(path, subfile)
            try:
                files.append(FSNode(os.path.split(subfile)[1],
                                    subfile,
                                    os.path.getsize(subfile)
                                    )
                             )
            except OSError as e:
                errors.append(subfile)
                
    heapq.heapify(files)
    return [heapq.heappop(files) for i in range(len(files))]


def heapify_dir(root='/'):
    if not os.path.isdir(root):
        raise Exception(root, 'should be a dir')
    files = []
    errors = []
    for path, subdirs, subfiles in os.walk(root):
        for subfile in subfiles:
            subfile = os.path.join(path, subfile)
            try:
                files.append(FSNode(os.path.split(subfile)[1],
                                    subfile,
                                    os.path.getsize(subfile)
                                    )
                             )
            except OSError as e:
                errors.append(subfile)               
    heapq.heapify(files)
    return files

def get_one_page(heap, items=10):
    result = []
    for i in range(items):
        if len(heap) == 0:
            return result
        result.append(heapq.heappop(heap))
    return result


if __name__ == "__main__":
    root = FSNode(abs_path="/Users/rujia/python")
    traverse(root)

