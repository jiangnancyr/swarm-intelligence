import math
import numpy as np
import copy
import random
import swarmParas as ap
import sys
import scipy.io as scio

"""
初始化的方式是范围是在生活区以内，方向随机，速度大小小于闲散速度vComf
"""
class swarmInitStatus ():
    def __init__ (self,
                  livingR = ap.livingR,
                  vComf = ap.vComf):
        self.livingR = livingR
        self.vComf = ap.vComf
        self.prey = ap.prey
        self.predator = ap.predator
        
        self.preyPositions = np.zeros((self.prey, 2))  #存放的是位置
        self.preySpeeds = np.zeros((self.prey, 1))     #存放的是速度的大小
        self.preyDirections = np.zeros((self.prey, 2))  #存放的是方向

        self.predatorPositions = np.zeros((self.predator, 2))  #存放的是位置
        self.predatorSpeeds = np.zeros((self.predator, 1))     #存放的是速度的大小
        self.predatorDirections = np.zeros((self.predator, 2))  #存放的是方向

        
    def createPrey (self):
        if ap.k == 0:
            for i in range(ap.prey):
                #生成位置坐标
                self.preyPositions[i][0] = random.uniform(0, ap.lengthX)
                self.preyPositions[i][1] = random.uniform(0, ap.lengthY)
                #速度大小
                self.preySpeeds[i][0] = 1
            
                #生成随机方向
                angle = random.uniform(0, 2*math.pi)
                self.preyDirections[i][0] = math.cos(angle)
                self.preyDirections[i][1] = math.sin(angle)
        elif ap.k == 1:
            for i in range(ap.prey):
                angle = random.uniform(0, 2*math.pi)
                L = random.uniform(0, (ap.lengthX - 0.5)/2)
                self.preyPositions[i][0] = L*math.cos(angle) + ap.lengthX/2
                self.preyPositions[i][1] = L*math.sin(angle) + ap.lengthY/2
                #速度大小
                self.preySpeeds[i][0] = 1
            
                angleD = angle - math.pi/2
                self.preyDirections[i][0] = math.cos(angleD)
                self.preyDirections[i][1] = math.sin(angleD)
                
        return self.preyPositions, self.preySpeeds, self.preyDirections

    def createPredator (self):
        for i in range(ap.predator):
            #生成位置坐标
            angle = random.uniform(0, 2*math.pi)
            L = random.uniform(0, self.livingR)
            self.predatorPositions[i][0] = L*math.cos(angle)
            self.predatorPositions[i][1] = L*math.sin(angle)
            
            #速度大小
            self.predatorSpeeds[i][0] = random.uniform(0, self.vComf)

            #生成随机方向
            angle = random.uniform(0, 2*math.pi)
            self.predatorDirections[i][0] = math.cos(angle)
            self.predatorDirections[i][1] = math.sin(angle)
        return self.predatorPositions, self.predatorSpeeds, self.predatorDirections
        
        
    def useSameInitStatus (self):
        pass

    def initStatusSave(self, fileName='initStatus.mat'):
        
        self.createPrey()
        scio.savemat(fileName, {'preyPositions': self.preyPositions,
                                'preySpeeds': self.preySpeeds,
                                'preyDirections': self.preyDirections,
                                'messages':np.array([ap.lengthX, ap.lengthY,
                                                   ap.prey])})

    def initStatusGet(self, fileName='initStatus.mat'):
        parameters = scio.loadmat(fileName)
        self.preyPositions = parameters['preyPositions']
        self.preySpeeds = parameters['preySpeeds']
        self.preyDirections = parameters['preyDirections']
        self.messages = parameters['messages'][0]
        ap.lengthX = self.messages[0]
        ap.lengthY = self.messages[1]
        ap.prey = self.messages[2]
        return self.preyPositions, self.preySpeeds, self.preyDirections

