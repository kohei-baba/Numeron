import math
import random
class Numeron:
    #初期化
    def __init__(self,d):
        self.digit = d    #数字の桁数
        self.candidate = [i for i in range(10**(d-1),10**d) if self.valid(str(i))]
        self.left = [i for i in range(10**(d-1),10**d) if self.valid(str(i))]
        self.phase = 1
        self.flag = True
    #思い浮かべうる数字として適当なものだけを抽出
    def valid(self,n):
        if all(n[i] != n[j]  for j in range(0,self.digit-1) for i in range(j+1,self.digit)):
            return True
    #何EAT何BITEかを数える
    def check(self,x,y):
        eat = 0
        bite = 0
        for i in range(self.digit):
            xi = x[i]
            if xi in y:
                if y[i] == xi:
                    eat += 1
                else:
                    bite += 1
        return [eat,bite]
    #平均情報量を計算
    def entropy(self,x):
        xx = [0 for _ in range((self.digit+1)*self.digit+1)]
        for i in self.left:
            eat,bite = self.check(str(x),str(i))
            xx[(self.digit+1)*eat+bite] += 1
        return sum(xxi*math.log2(xxi) for xxi in xx if xxi != 0)
    #もっとも平均情報量が大きいものを見つける
    def bestentropy(self):
        if len(self.left) == 1:
            print("I am confident that your number is : ")
            return self.left[0]
        mn = float("inf")
        mnchoice = []
        for i in self.candidate:
            se = self.entropy(i)
            if se < mn:
                mn = se
                mnchoice = [i]
            elif se == mn:
                mnchoice.append(i)
        return random.choice(mnchoice)   
    #回答を元に候補を絞り込む  
    def narrow(self,x,reat,rbite):
        newleft = []
        for i in self.left:
            eat,bite = self.check(str(x),str(i))
            if reat == eat and rbite == bite:
                newleft.append(i)
        self.left = newleft
        return
    def aisturn(self):
        if self.phase == 1:
            while True:
                x = str(random.choice(self.candidate))
                if all(x[i] != 0 for i in range(self.digit)):
                    print(int(x))
                    reat,rbite = map(int,input().split())
                    if reat == self.digit:
                        print("I identified your number by "+str(self.phase)+" tries")
                        self.flag = False
                        return
                    self.narrow(int(x),reat,rbite)
                    self.phase += 1
                    return           
        sb = self.bestentropy()
        print(sb)
        reat,rbite = map(int,input().split())
        if reat == self.digit:
            print("I identified your number by "+str(self.phase)+" tries!")
            self.flag = False
            return
        self.narrow(sb,reat,rbite)
        self.phase += 1
        return
    def playgame(self):
        while self.flag:
            self.aisturn()
Numeron(4).playgame()