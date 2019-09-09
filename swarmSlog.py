import matplotlib.pyplot as plt
import random
import math
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import copy
import swarmParas as ap
import friendFun as fF
import swarmInit as si
import swarmPlot as sp

turnAngle = np.array([0.0, 0.0])
turnList = []
turnA = math.pi/2
"""
这一部分分为猎物和捕食者的算法，先开发猎物的算法，可合并
"""

def getParas(fileName='para.txt'):
    paras = []
    with open(fileName) as file_object:
        for line in file_object:
            paras.append(float(line))
    return paras

def saveRes (fileName,data):
    file_handle = open(fileName, mode='a')
    for i in range(len(data)):
        if i == 0:
            file_handle.writelines (str(data[i]))
        else:
            file_handle.writelines(',')
            file_handle.writelines (str(data[i]))
    file_handle.writelines('\r\n')
    file_handle.close()
"""
vicsek模型加速算法
"""
paras = getParas()
L = int(paras[0])
pNum = int(paras[1])
nbNum = np.zeros((L,L,pNum))#将环境拆分成格子
nbSize = np.zeros((L,L))#记录每个格子粒子数目
class preySlog ():
    def __init__ (self, n):
        self.n = n
        self.newpyd = np.array([0.0, 0.0])
        self.newpys = np.array([0.0]) 
        self.newpyp = np.array([0.0, 0.0])
        self.fuzzy = fF.friendFuns ()
        self.nbList = np.zeros(pNum)
        self.nbNum = 0

    def getNbList(self,
                  preyPositions):
        self.nbList = np.zeros(pNum)
        self.nbNum = 0
        global nbNum, nbSize, L
        for i in range(3):
            for j in range(3):
                if j == 1:
                    tempx = int(preyPositions[self.n][0])
                elif j == 0:
                    tempx = int(preyPositions[self.n][0]) - 1
                    if tempx < 0:
                        tempx = L - 1
                elif j == 2:
                    tempx = int(preyPositions[self.n][0]) + 1
                    if tempx >= L:
                        tempx = 0
                if i == 1:
                    tempy = int(preyPositions[self.n][1])
                elif i == 0:
                    tempy = int(preyPositions[self.n][1]) + 1
                    if tempy >= L:
                        tempy = 0
                elif i == 2:
                    tempy = int(preyPositions[self.n][1]) - 1
                    if tempy < 0:
                        tempy = L - 1
                if tempy == L:
                    tempy = L - 1
                if tempx == L:
                    tempx = L - 1

                kNum = int(nbSize[tempy][tempx])

                for s in range(kNum):
                    self.nbList[self.nbNum] = int(nbNum[tempy][tempx][s])
                    self.nbNum += 1                                         #个数加一

        
        
    def Vicsek_base (self,
                     preyPositions,
                     preySpeeds,
                     preyDirections,
                     time_step=0.1,
                     openflag=0,
                     a=0):
        global turnAngle, turnList
        self.newpyd = np.array([0.0, 0.0])
        self.newpys = np.array([0.0])
        self.newpyp = np.array([0.0, 0.0])
        r = 1
        L = ap.lengthX
        self.getNbList(preyPositions)
                
##        for num in range(ap.prey):
        for p in range(self.nbNum):
            num = int(self.nbList[p])
            kflag = 0
            if num != self.n:       
                rx = abs(preyPositions[self.n][0] - preyPositions[num][0])
                ry = abs(preyPositions[self.n][1] - preyPositions[num][1])
                
                if rx <= r and ry <= r:
                    if math.hypot(rx, ry) <= r:
                        kflag = 1
                   
                elif L - rx <= r and ry <= r:
                    rx = L - rx
                    if math.hypot(rx, ry) <= r:
                        kflag = 1
                  
                elif rx <= r and L - ry <= r:
                    ry = L - ry
                    if math.hypot(rx, ry) <= r:
                        kflag = 1
                    
                elif L - rx <= r and L - ry <= r:
                    ry = L - ry
                    rx = L - rx
                    if math.hypot(rx, ry) <= r:
                        kflag = 1
                    
                if kflag == 1:
##                    print(num)
                    speedDir = copy.deepcopy(preyDirections[num])
                    npd = np.array([0.0, 0.0])
                    if ap.perNoiseFlag == 1:
                        perNoise = random.uniform(-ap.perNoiseRate*math.pi, ap.perNoiseRate*math.pi)
                        npd[0] = speedDir[0]*math.cos(perNoise)\
                                + speedDir[1]*math.sin(perNoise)
                        npd[1] = -speedDir[0]*math.sin(perNoise)\
                                + speedDir[1]*math.cos(perNoise)
                    else:
                        npd[0] = speedDir[0]
                        npd[1] = speedDir[1]
                        
                    cosAngle = npd[0] * preyDirections[self.n][0] \
                                + npd[1] * preyDirections[self.n][1]
                    if cosAngle > 1:
                         cosAngle = 1
                    elif cosAngle < -1:
                        cosAngle = -1
                    if openflag == 1:
                        angle = math.acos(cosAngle)
                        npd *= self.fuzzy.bestAngle(angle, a) * (1 - ap.baseImport)\
                                    + ap.baseImport
                    self.newpyd += npd
                    
        speedDir = copy.deepcopy(preyDirections[self.n])
        self.newpyd += speedDir
        if self.newpyd[1] == 0 and self.newpyd[0] == 0:
            self.newpyd = np.array([0, 0])
            print('error!')
        else:
            forceSize = math.sqrt(self.newpyd[0] ** 2 + self.newpyd[1] ** 2)
            self.newpyd /= forceSize
        cosTa = np.dot(self.newpyd, speedDir)
        if cosTa < math.cos(ap.maxTurn):
            #大于最大转动角
            mt = ap.maxTurn
            if speedDir[1]*self.newpyd[0] > speedDir[0]*self.newpyd[1]: 
                mt = -ap.maxTurn#逆时针
                
            self.newpyd[0] = speedDir[0]*math.cos(mt)\
                            - speedDir[1]*math.sin(mt)
            self.newpyd[1] = speedDir[0]*math.sin(mt)\
                            + speedDir[1]*math.cos(mt)

        self.newpys[0] = 1
        self.newpyp = preyPositions[self.n] +  time_step*self.newpyd
        
        if self.newpyp[0] < 0:
            self.newpyp[0] += ap.lengthX
        elif self.newpyp[0] > ap.lengthX:
            self.newpyp[0] = ap.lengthX - self.newpyp[0]
        if self.newpyp[1] < 0:
            self.newpyp[1] += ap.lengthY
        elif self.newpyp[1] > ap.lengthY:
            self.newpyp[1] = ap.lengthY - self.newpyp[1]
        return self.newpyp, self.newpys, self.newpyd
            
def createInitData (l=5, n=300, number=1):
    ap.prey = n
    ap.lengthX = l
    ap.lengthY = l
    dataInit = si.swarmInitStatus()
    name = 'initdatas/initData'
    for i in range(number):
        pathname = name + str(l) + '_' + str(n) + '_' + str(i) +'.mat'
        dataInit.initStatusSave(pathname)

plotShow = '0'
def main (usefile='1', filename='initdatas/initData0.mat', a=0, openflag=0):
    global nbNum, nbSize, turnAngle, turnList, turnA
    single = {}
    initData = si.swarmInitStatus()
    if usefile == '0':
        preyPositions, preySpeeds, preyDirections = initData.createPrey()
    elif usefile == '1':
        preyPositions, preySpeeds, preyDirections = initData.initStatusGet(filename)
        ap.prey = len(preyPositions)
     
    preySize = 0.1
    preyColor = ['b' for i in range(ap.prey)]
    
    for i in range(ap.prey):
        single[i] = preySlog(i)
    if plotShow == '1':
        sda = sp.swarmDrawAgent2D('flocking simulation', lengthX=ap.lengthX,
                              lengthY=ap.lengthY)
    #初始化一下
    nbNum = np.zeros((L,L,pNum))#将环境拆分成格子
    nbSize = np.zeros((L,L))#记录每个格子粒子数目 
    for i in range(ap.prey):
        intX = int(preyPositions[i][0])
        intY = int(preyPositions[i][1])
        nbNum[intY][intX][int(nbSize[intY][intX])] = i
        nbSize[intY][intX] += 1  
    step = 0
    synData = []
    s = np.array([0.0, 0.0])
    for i in range(ap.prey)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               :
        s += preyDirections[i]
    syn = math.sqrt(s[0]**2 + s[1]**2)/ap.prey
    print('step = '+ str(step))
    print('syn = ' + str(syn))
    synData.append(syn)
    while True:
        if plotShow == '1':
            sda.drawPrey (preyPositions,
                          preyDirections,
                          preyColor,
                          preySize)
            sda.pause(0.01)
        for i in range(ap.prey):
            single[i].Vicsek_base(preyPositions,
                                  preySpeeds,
                                  preyDirections,
                                  time_step=ap.stepTime,
                                  openflag=openflag,
                                  a=a*math.pi/8)
            
        nbNum = np.zeros((L,L,pNum))#将环境拆分成格子
        nbSize = np.zeros((L,L))#记录每个格子粒子数目
        for i in range(ap.prey):
            preyPositions[i][0] = single[i].newpyp[0]
            preyPositions[i][1] = single[i].newpyp[1]
            preySpeeds[i][0] = single[i].newpys[0]
            preyDirections[i][0] = single[i].newpyd[0]
            preyDirections[i][1] = single[i].newpyd[1]
            #统计每格数量
            
            intX = int(preyPositions[i][0])
            intY = int(preyPositions[i][1])
            nbNum[intY][intX][int(nbSize[intY][intX])] = i
            nbSize[intY][intX] += 1
        if plotShow == '1':    
            sda.clearPrey()
        step += 1
        s = np.array([0.0, 0.0])
        for i in range(ap.prey)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               :
            s += preyDirections[i]
        syn = math.sqrt(s[0]**2 + s[1]**2)/ap.prey
        print('step = '+ str(step))
        print('syn = ' + str(syn))
        synData.append(syn)
        if step >= ap.stepRun:
            return synData
        

def read_datas (filename):
    datas = []
    with open(filename) as file_object:
        for line in file_object:                    #读取数据的一行
            line = line.rstrip()                #除去换行符
            line = line.split(',')              #以‘ ’拆分
            data =  [float(i) for i in line]    #化成浮点
            datas.append(data)                  #添加到新的数据
        return datas
#运行n步保存数据最后统一画图。
#每次运行保存一个同步数据再数组中，数组大小确定
    
if __name__ == '__main__':
    #createInitData(l=3, n=100, number=10)
    name = 'initdatas/initData'
    paras = getParas()
    ap.baseImport = paras[2]            #基础关注度设置
    ap.stepRun = paras[3]               #运行步数设置
    resDatas = [[0 for i in range(200)] for i in range(10)] #第一个数字是表示第几个数据
    i = 2  #采用第几组数据
    dp = sp.drawPlot(title = '  ',sr=ap.stepRun)
    for j in range(0,10):#0:原始模型；1到9:表示从关注角从0到pi
        pathname = name + str(int(paras[0])) + '_' + str(int(paras[1])) + '_' + str(i) +'.mat'
        if j == 0:
            openflag = 0#[2, 78, 59, 44, 27, 26, 22, 17, 29, 51, 36]
        else:           #[1, 64, 38, 28, 28, 38, 38, 49, 61, 25, 28]
            openflag = 1#[0, 40, 42, 38, 30, 30, 28, 16, 17, 77, 25]
        if j%1 == 0:
            resDatas[j] = main(usefile='1',
                               filename=pathname,
                               a=(j - 1),
                               openflag=openflag)
##            dp.legendShow ()
            dp.drawRes(resDatas[j],j)

        svaefileName = 'resdatas/resdata' + str(int(paras[0])) + '_'\
                       + str(int(paras[1]))+ '_'+ str(ap.baseImport) + \
                       '_compare_' + str(i)+  '.txt'
        print(len(resDatas[j]))
        saveRes(svaefileName, resDatas[j])
    
    
##    Y = read_datas(svaefileName)
##    for i in range(len(Y)):
##        if i%2 == 0:
##            dp.drawRes(Y[i])
    
    

                        
                        
                        
                        
                        
                        
            
        
