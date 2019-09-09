import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib import cm
import swarmParas as ap

colorChose = {0 : '#000000',6: '#a20055',12 : '#cc0000',18 : '#ff5511',
			  1 : '#ffaa33',7: '#ffdd55',13: '#ffff33',19: '#bbff00',
			  2 : '#66dd00',8: '#00aa00',14: '#008844',20 : '#00aa55',
			  3: '#00ddaa',19 : '#00ffff',15: '#33ccff',21: '#99bbff',
			  4: '#5555ff',10 : '#5500ff',16 : '#5500dd',22 : '#66009d',
			  5: '#660077',11 : '#990099',17 : '#ff3eff',23 : '#ffb3ff',
			  }
class friendFuns ():
    def __init__ (self):
        pass
    #正S曲线隶属度函数
    def FuzzyFunS1 (self, x, a, b, c):
        if x < a:
            return 0
        elif a <= x  and x <= b:
            return 2*((x - a)/(c - a))**2
        elif b < x and x <= c:
            return 1 - 2*((x - c)/(c - a))**2
        else:
            return 1

    #反S曲线隶属度函数
    def FuzzyFunS2 (self, x, a, b, c):
        if x < a:
            return 1
        elif a <= x  and x <= b:
            return 1 - 2*((x - a)/(c - a))**2
        elif b < x and x <= c:
            return 2*((x - c)/(c - a))**2
        elif x > c:
            return 0
    def FuzzyFunS12 (self, x, p=0, w=math.pi):
        if x < p:
            return self.FuzzyFunS1(x, p - w/2, p - w/4, p)
        else:
            return self.FuzzyFunS2(x, p, p + w/4, p + w/2)
        
    def trapezoidFun (self, x, a, b, c, d):
        if x < a:
            return 0
        elif x >= a and x < b:
            return (x - a)/(b - a)
        elif x >= b and x < c:
            return 1
        elif x >= c and x < d:
            return (d - x)/(d- c)
        elif x >= d:
            return 0

    def front (self, x):
        return self.trapezoidFun (x, -math.pi/4, 0, math.pi/4, math.pi/2)
    def rl_front (self, x):
        return self.trapezoidFun (x, 0, math.pi/4, math.pi/2, math.pi*3/4)
    def rl_behind (self, x):
        return self.trapezoidFun (x, math.pi/4, math.pi/2, math.pi*3/4, math.pi)
    def behind (self, x):
        return self.trapezoidFun (x, math.pi/2, math.pi*3/4, math.pi, math.pi*5/4)
    def andFun (self, a, b):
        if a > b:
            return b
        else:
            return a

    def orFun (self, a, b):
        if a > b:
            return a
        else:
            return b
    def bestAngle(self, x, a=0):
        if x < 0:
            print ('angle error!')
            return 0

        return self.FuzzyFunS12(x, p=a, w=math.pi)
##        if a == 0:
##            return self.front(x)
##        elif a == 1:
##            return self.orFun(self.front(x), self.rl_front(x))
##        elif a == 2:
##            return self.orFun(self.rl_front(x), self.rl_beind(x)) 
##        elif a == 3:
##            res = self.orFun(self.front(x), self.rl_front(x))
##            return self.orFun(res, self.rl_behind(x))
##        elif a == 4:
##            return 1
##        elif a == 5:
##            res = self.orFun(self.behind(x), self.rl_behind(x))
##            return self.orFun(res, self.rl_front(x))
##        elif a == 6:
##            return self.orFun(self.behind(x), self.rl_behind(x))
##        elif a == 7:
##            return self.behind(x)

        
##        if a == 0:
##            return self.FuzzyFunS2(x, 0, (a + math.pi/8)/2, a + math.pi/8)
##        elif a == math.pi:
##            return self.FuzzyFunS1(x, math.pi*7/8, (a + math.pi*7/8)/2, a)
##        else:
##            if x <= a:
##                return self.FuzzyFunS1(x, a - math.pi/8, (2*a - math.pi/8)/2, a)
##            else:
##                return self.FuzzyFunS2(x, a, (2*a + math.pi/8)/2, a + math.pi/8)
##        if x <= a:
##            if x == 0:
##                return 0
##            else:
##                return self.FuzzyFunS1 (x, 0, a/2, a)
##        else:
##            if x == math.pi:
##                return 0
##            else:
##                return self.FuzzyFunS2 (x, a, (math.pi + a)/2, math.pi)
            
    #画隶属度函数图操作   
    def  drawPlot (self, function, interval = 0.1, xlim = [0,20]):
        fig = plt.figure()          #制作图表fig
        ax1 = fig.add_subplot(111)  #当前画布切成3行3列，本图占1块ax1
        plt.title('FuzzyFunction')
        ax1.set_xlim(xlim[0], xlim[1])
        ax1.set_ylim(0, 1.1)
        n = int((xlim[1] - xlim[0])/interval)
        X = np.array([xlim[0] + i*interval for i in range(n)])
        Y = np.array([0.0 for i in range(n)])#要浮点才可以传递数
        color = 0
        for fun in function:
            color += 1
            for i in range(n):
                Y[i] = fun(xlim[0] + i*interval)
            ax1.plot(X, Y,label='FuzzyFunction' + str(i+1),linewidth=1,color=colorChose[color],
                markerfacecolor='blue')
        plt.pause(0.01)

    def plotShow(self):
        funlist = [self.bestAngle]
        self.drawPlot(funlist, interval = 0.01, xlim = [0,math.pi*1.2])
          

        
def main ():
    ff = friendFuns()
    ff.plotShow()

if __name__ == '__main__':
    main()
    


    
            
        
