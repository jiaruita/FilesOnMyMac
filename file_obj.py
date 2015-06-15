import os
import heapq
from collections import deque

class FSNode(object):
    def __init__(self, name=None, abs_path=None, size=None):
        self.abs_path = abs_path
        self.name = os.path.split(abs_path)[-1] if name is None else name
        self.size = 0 if size is None else size
        self.children = []

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
        Get the list of entry names under a directory.
        :return
            a list of strings, each of which is the name without path
        """
        if not os.path.isdir(self.abs_path):
            raise Exception(str(self.abs_path) + ' should be a dir')
        return os.listdir(self.abs_path)


class DirObj(FSNode):
    pass


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


    
