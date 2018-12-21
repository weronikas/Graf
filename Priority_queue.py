import math
import random

class Priority_queue:


    def __init__(self):
        self.pq = [None]
        self.dic = {}

    def insert (self, m):
        if m[1] not in self.dic:
            self.pq.append(m)
            self.dic[m[1]] = len(self.pq) - 1
            self.swim(len(self.pq) - 1)
        else:
            print ("Juz jest element o podanym ID")


    def getmin (self):
#        if not self.isempty:
        min = self.pq[1]
        self.dic.pop(self.pq[1][1])
        if (len(self.pq) > 2):
            self.pq[1] = self.pq[-1]
            self.dic[self.pq[1][1]] = 1
        self.pq.pop()
        self.sink(1)
        return min
#        else:
#            raise Exception('Priority queue is empty')

    def decrease (self, m):
        if m[1] in self.dic:
            if (m[0] < self.pq[self.dic[m[1]]][0]):
                self.pq[self.dic[m[1]]] = m
                self.swim(self.dic[m[1]])
        else:
            print ("Nie ma elementu o podanym ID")


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

    def test_correct (self):
        k = len(self.pq) - 1
        while (k  >= 2):
            if self.pq[k][0] < self.pq[int(math.floor(k / 2))][0]:
                print "Blad kopca pq przy k = " + str(k)
            #nie testuje k=1
            if self.dic[self.pq[k][1]] != k:
                print "Blad slownika przy k = " + str(k)
            k -= 1



def random_test(num):
    Pqueue = Priority_queue()
    for i in range(num):
        if len(Pqueue.pq) == 1:
            elem = (random.randint(1,100000), random.randint(1,10000))
            Pqueue.insert(elem)
            #print "Insert: " + str(elem)
        else:
            prob = random.randint(1,4)
            if prob < 3:
                id1 = random.randint(1, 10000)
                while id1 in Pqueue.dic:
                    id1 = random.randint(1, 10000)
                elem = (random.randint(1, 100000), id1)
                Pqueue.insert(elem)
                #print "Insert: " + str(elem)
            elif prob < 4:
                Pqueue.getmin()
                #print "Getmin"
            else:
                new_pq = Pqueue.pq[1:]
                random.shuffle(new_pq)
                ind = new_pq[0][1]
                elem = (random.randint(1, 100000), ind)
                Pqueue.decrease(elem)
                #print "Decrease: " + str(elem)
    print Pqueue
    Pqueue.test_correct()







if __name__ == "__main__":
    """
    P = Priority_queue()
    print 'Kolejka priorytetowa: ' + str(P)
    P.insert((4,0))
    print 'Kolejka priorytetowa: ' + str(P)
    P.insert((6,9))
    P.decrease((3,0))
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
    P.decrease((8,4))
    a = P.getmin()
    a = P.getmin()
    print 'Kolejka priorytetowa: ' + str(P)
    print 'a: ' + str(a)
    P.test_correct()
    """

    random_test(10)
