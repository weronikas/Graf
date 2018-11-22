class Priority_queue:


    def __init__(self):
        self.pq = [None]
        self.dic = {}
        self.p = {}

    def insert (self, m, earlier):
            if m[1] in self.dic:
                if (m[0] < self.pq[self.dic[m[1]]][0]):
                    self.pq[self.dic[m[1]]] = m
                    self.p[m] = earlier
            self.pq.append(m)
            self.dic[m[1]] = len(self.pq) - 1
            self.swim(len(self.pq) - 1)


    def getmin (self):
#        if not self.isempty:
        min = self.pq[1]
        del self.dic[self.pq[1][1]]
        self.pq[1] = self.pq[-1]
        self.dic[self.pq[1][1]] = 1
        self.pq.pop()
        self.sink(1)
        return min
#        else:
#            raise Exception('Priority queue is empty')

    def decrease (self, m):
        pass


    def isempty (self):
        if (len(self.pq) == 1):
            return True
        else:
            return False

    def swim (self, k):
        while (k > 1 and self.pq[k][0] < self.pq[k / 2][0]):
            self.exch(k, k/2)
            k = k / 2

    def sink (self, k):
        while (2 * k <= (len(self.pq) - 1)):
            j = 2 * k
            if (j < (len(self.pq) - 1)) and (self.pq[j][0] > self.pq[j + 1][0]):
                j += 1
            if self.pq[k][0] <= self.pq[j][0]:
                break
            self.exch(k, j)
            k = j

    def exch (self, a, b):
        temp = self.pq[a]
        self.pq[a] = self.pq[b]
        self.pq[b] = temp
        self.dic[self.pq[a][1]] = a
        self.dic[self.pq[b][1]] = b

    def __str__(self):
        pq_str = ''
        for elem in self.pq:
            pq_str +=  ' ' + str(elem)
        for key, value in self.dic.iteritems():
            pq_str +=  ' ' + 'Key: ' + str(key) + ' Value: ' + str(value)
        return pq_str


"""
P = Priority_queue()
print 'Kolejka priorytetowa: ' + str(P)
P.insert((4,0))
print 'Kolejka priorytetowa: ' + str(P)
P.insert((6,9))
P.insert((3,0))
P.insert((12,1))
P.insert((7,3))
print 'Kolejka priorytetowa: ' + str(P)
a = P.getmin()
print 'Kolejka priorytetowa: ' + str(P)
print 'a: ' + str(a)
P.insert((1,43))
P.insert((5,51))
P.insert((13,44))
P.insert((7,43))
print 'Kolejka priorytetowa: ' + str(P)
a = P.getmin()
print 'Kolejka priorytetowa: ' + str(P)
print 'a: ' + str(a)
b = P.isempty()
print str(b)
P.insert((25,4))
P.insert((3,41))
P.insert((8,4))
a = P.getmin()
a = P.getmin()
print 'Kolejka priorytetowa: ' + str(P)
print 'a: ' + str(a)
"""