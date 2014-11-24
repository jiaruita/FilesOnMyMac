import os
import heapq
from collections import deque
class FileObj(object):
    def __init__(self, name=None, path=None, size=None):
        self.name = name
        self.path = path
        self.size = size

    def __lt__(self, other):
        return self.size < other.size


class DirObj(FileObj):
    pass




def get_list(path):
    if not os.path.isdir(path):
        raise Exception(path , 'should be a dir')
    return os.listdir(path)
        

def sort_all():
    files = []
    errors = []
    for path, subdirs, subfiles in os.walk('/'):
        for subfile in subfiles:
            subfile = os.path.join(path, subfile)
            try:
                files.append(FileObj(os.path.split(subfile)[1], subfile, os.path.getsize(subfile)))
            except OSError, e:
                errors.append(subfile)
                
    heapq.heapify(files)
    return [heapq.heappop(files) for i in range(len(files))]


    
    
    
