import numpy as np
from random import randint
from matplotlib import pyplot as plt 
class state:
    def __init__(self,batteryMax):
        self.x=0
        self.y=0
        self.batteryMax=batteryMax
        self.battery=self.batteryMax
        self.lastAction=0

    def run(self,action,map):
        newState=[self.x,self.y,self.battery-1,self.lastAction]
        if(action==0):
            newState[1]+=1
        if(action==1):
            newState[0]+=1
        if(action==2):
            newState[1]-=1
        if(action==3):
            newState[0]-=1
        if(map.valid(newState)):
            map.cleaned[newState[1],newState[0]]=1
            self.x=newState[0]
            self.y=newState[1]
            self.battery=newState[2]
            self.lastAction=action
            return True
        else:
            return False
    
    def init(self):
        self.x=0
        self.y=0
        self.battery=self.batteryMax
    def getState(self):
        return [self.x,self.y,self.battery,self.lastAction]
    
    def end(self):
        if(self.battery==0):
            return True
        else:
            return False
    
    def set(self,newState):
        self.x=newState[0]
        self.y=newState[1]
        self.battery=newState[2]
class map:
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.map=np.zeros((x,y))
        self.cleaned=np.zeros((x,y))
        self.cleaned[0,0]=1
        #self.wall()
    
    #function for creating walls
    def wall(self):
        self.map[0:4,4]=3
        self.cleaned[0:4,4]=3
    #initialize the cleaned map
    def init(self):
        self.cleaned=np.zeros((self.x,self.y))
        self.cleaned[0,0]=1
        #self.wall()
    
    def valid(self,newState):
        if(newState[0]<0 or newState[0]>=self.x or newState[1]<0 or newState[1]>=self.y or self.cleaned[newState[1],newState[0]]==3):
            return False
        else:
            return True
    def show(self,state):
        board=self.cleaned.copy()
        board[state[1],state[0]]=2
        plt.cla()
        plt.imshow(board,origin="lower")
        plt.pause(0.1)
    def complete(self):
        if(self.cleaned.min()==0):
            return False
        else:
            return True

if __name__=="__main__":
    room=map(10,10)
    clean_robot=state()
    while(True):
        clean_robot.run(randint(0,3),room)
        
        room.show(clean_robot.getState())
        if(clean_robot.end()):
            exit()
