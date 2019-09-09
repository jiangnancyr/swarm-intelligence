import matplotlib.pyplot as plt
import random
import math
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os
import sys
import scipy.io as scio

import swarmParas as ap
import swarmInit as si

class swarmDrawAgent2D ():

    def __init__ (self,
                  graphName='',
                  lengthX=ap.lengthX,
                  lengthY=ap.lengthY,
                  livingR=ap.livingR,
                  timeInterval=ap.timeInterval):
        
        self.lengthX = lengthX
        self.lengthY = lengthY
        self.livingR = livingR
        self.title = graphName           #图标标题
        self.fig = plt.figure()          #制作图表fig
        self.ax = {}
        self.ax[0] = self.fig.add_subplot(111)  #当前画布切成1行1列，本图占1块ax1
        self.ax[0].set_xlabel('x')           #坐标轴加标签
        self.ax[0].set_ylabel('y')
        plt.title(self.title)                    #加上标题
        
        self.msgPrey = {}  #save position of the agent 
        self.msgPredator = {} #save direction of agent
        self.timeInterval = timeInterval
        self.k = 0
        self.ax[0].set_ylim(0, self.lengthX)
        self.ax[0].set_xlim(0, self.lengthY)
    def drawLiving (self, internal=60,c='y'):
        x = [0, 0]
        y = [0, 0]
        cta = 2*math.pi/internal
        for i in range(internal):
            angle0 = i*cta
            angle1 = (i + 1)*cta
            x[0] = self.livingR*math.cos(angle0)
            y[0] = self.livingR*math.sin(angle0)
            x[1] = self.livingR*math.cos(angle1)
            y[1] = self.livingR*math.sin(angle1)
            self.ax[0].plot(x,
                            y,
                            linewidth=1,
                            color=c,
                            markerfacecolor=c)
        
            
    def drawPrey (self,
                  preyPositions,
                  preyDirection,
                  preyColor,
                  preySize):
        number = len(preyPositions)
        for i in range(number):
            self.msgPrey[i] = self.ax[0].arrow(preyPositions[i][0],
                                       preyPositions[i][1],
                                       preyDirection[i][0]*preySize,
                                       preyDirection[i][1]*preySize,
                                       width=0.01,
                                       length_includes_head=True, # 增加的长度包含箭头部分
                                       head_width=0.5*preySize,
                                       head_length=1*preySize,
                                       fc=preyColor[i],
                                       ec=preyColor[i],
                                       alpha=0.8)

    def drawPredator (self,
                      predatorPositions,
                      predatorDirection,
                      predatorColor,
                      predatorSize):
        number = len(predatorPositions)
        for i in range(number):
            self.msgPredator[i] = self.ax[0].arrow(predatorPositions[i][0],
                                       predatorPositions[i][1],
                                       predatorDirection[i][0],
                                       predatorDirection[i][1],
                                       width=0.01,
                                       length_includes_head=True, # 增加的长度包含箭头部分
                                       head_width=0.5*predatorSize,
                                       head_length=1*predatorSize,
                                       fc=predatorColor[i],
                                       ec=predatorColor[i],
                                                   alpha=0.8)
        
        
    def clearPrey (self):
        for i in range(ap.prey):
            self.msgPrey[i].remove()
    def clearPredator (self):
        for i in range(ap.predator):
            self.msgPredator[i].remove()
            
    def pause(self, time=0.1):
        plt.pause(time)
        
    def clearAll (self):
        self.fig.clear()
"""
　　八种内建默认颜色缩写
　　b: blue
　　g: green
　　r: red
　　c: cyan
　　m: magenta
　　y: yellow
　　k: black
　　w: white
"""
colors = {  0:'r',
            1:'g',
            2:'y',
            3:'c',
            4:'m',
            5:'b',
            6:'k',
            7:'#005566',
            8:'#445566',
            9:'#445500',
            10:'#440066',}

class drawPlot():
    def __init__(self,title = '  ',sr=ap.stepRun):
        self.title = title
        self.lineX = [i for i in range(int(sr) + 1)]
        self.fig = plt.figure()          #制作图表fig
        self.ax = self.fig.add_subplot('111')
        plt.title(self.title)  
        self.colornum = 0

    def drawRes (self, dataY, j):
        if j == 0:
            labelx = r'$VM$'
        else:
            labelx = r'$\beta=' + str((j - 1)*0.125) + r'\pi$'
        self.ax.plot(self.lineX,
                     dataY,
                     label=labelx,
                     linewidth=1,
                     color=colors[self.colornum],
                     markerfacecolor=colors[self.colornum])
        
        self.colornum += 1
        self.ax.legend()
        plt.pause(0.01)
        
    def legendShow (self):
        self.ax.legend()
        
    def pause (self):
        plt.pause(0.01)
        
def main():
    initData = si.swarmInitStatus()
    preyPositions, preySpeeds, preyDirections = initData.createPrey()
    predatorPositions, predatorSpeeds, predatorDirections = initData.createPredator()
    predatorSize = 0.3
    preySize = 0.1
    predatorColor = ['r' for i in range(ap.predator)]
    preyColor = ['b' for i in range(ap.prey)]
    sda = swarmDrawAgent2D('flocking simulation')
    sda.drawLiving(c='c')
    sda.drawPredator (predatorPositions,
                      predatorDirections,
                      predatorColor,
                      predatorSize)
    
    sda.drawPrey (preyPositions,
                  preyDirections,
                  preyColor,
                  preySize)
    
    sda.pause(1)

    dp = drawPlot(title = 'synchronization ',sr=ap.stepRun)
    Y = [i**1.5 for i in range(ap.stepRun + 1)]
    dp.drawRes(Y)
    Y = [i**1 for i in range(ap.stepRun + 1)]
    dp.drawRes(Y)
    

if __name__ ==  '__main__':
    main()
