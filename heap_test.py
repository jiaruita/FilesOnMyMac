import heapq

class A(object):
    def __init__(self, size):
        self.size = size

    def __cmp__(self, other):
        if self.size > other.size:
            return 1
        if self.size < other.size:
            return -1
        if self.size == other.size:
            return 0
    def __lt__(self, other):
        return self.size < other.size

    def __eq__(self, other):
        return self.size == other.size

    def __ne__(self,other):
        return self.size != other.size

    def __le__(self, other):
        return self.size <= other.size

    def __gt__(self, other):
        return self.size > other.size

    def __ge__(self, other):
        return self.size >= other.size
    
    def __str__(self):
        return str(self.size)

    def __repr__(self):
        return str(self.size)

def test():
    l = [A(5), A(2), A(3)]
    print l
    h = []
    for i in l:
        heapq.heappush(h, i)
    print h

    nh = []
    for i in range(len(h)):
        nh.append(heapq.heappop(h))
    print nh

