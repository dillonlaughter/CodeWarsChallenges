class person(object):
    def __init__(self,cur,des):
        self.des = des
        self.cur = cur
        self.ignore = False
        if cur>des:
            self.button = 'down'
        if cur<des:
            self.button = 'up'
        if cur == des:
            self.button = 'none'
            self.ignore = True
        
    def update(self,cur):
        self.cur = cur
        if self.des == self.cur:
            self.ignore = True
            self.button = 'none'
            
class Dinglemouse(object):

    def __init__(self, queues, capacity):
        print(queues,capacity)
        self.q = []
        for i in range(len(queues)):
            self.q.append([])
            for j in range(len(queues[i])):
                self.q[-1].append(person(i,queues[i][j]))
        self.q.append([])
        self.cap = capacity
        self.ele = []
        self.cur = 0
        self.dir = 'up'
        self.fin = []
        self.ppl = []

        
    def theLift(self):
        self.check()
        if len(self.fin) == 0:
            self.fin.append(0)
        while True:
            b=0
            a= self.q+[self.ele]
            for i in range(len(a)):
                for j in a[i]:
                    if j.ignore == False:
                        b = 1
                        break
                if b == 1:
                    break
            if b == 0:
                break
            if self.dir == 'up':
                self.up()
            elif self.dir == 'down':
                self.down()
        if self.fin[-1]!=0:
            self.fin.append(0)
        fin = []
        for i in range(len(self.fin)-1):
            if self.fin[i] != self.fin[i+1]:
                fin.append(self.fin[i])
        fin.append(self.fin[-1])
        return fin

    def up(self):
        if self.cur >= len(self.q)-1:#if too high down
            self.dir = 'down'
            return
        self.cur+=1
        self.check()
    def down(self):
        if self.cur < 0:#if too low,up
            self.dir = 'up'
            return
        self.cur-=1
        self.check()

    def check(self):
        changed = 0
        for i in range(len(self.ele)-1,-1,-1):
            if self.ele[i].des == self.cur: #someone on elevator wants this floor
                self.q[self.cur].append(self.ele[i])
                self.q[self.cur][-1].update(self.cur)
                self.ele.remove(self.ele[i])
                changed = 1
        self.toremove = []
        for i in range(len(self.q[self.cur])):
            if self.q[self.cur][i].ignore == True:
                continue
            if self.q[self.cur][i].button == self.dir:#check bound errors
                if self.cap > len(self.ele):
                    self.ele.append(self.q[self.cur][i])
                    self.toremove.append(self.q[self.cur][i])
                changed = 1
        for i in self.toremove:
            self.q[self.cur].remove(i)
        if changed == 1:
            self.fin.append(self.cur)

    
