import robot
import numpy as np
class simulator:
    def __init__(self,algorithme):
        self.algorithme=algorithme
    def simulate(self,state,action,map):
        newState=state.copy()
        if(state[2]<=0):
            return -100,1,newState
        newState[2]-=1
        if(action==0):
            newState[1]+=1
        if(action==1):
            newState[0]+=1
        if(action==2):
            newState[1]-=1
        if(action==3):
            newState[0]-=1
        newState[3]=action
        if(not map.valid(newState)):
            newState=state.copy()
            #newState[2]-=1
            return -100,1,newState
        if(state[3]+2==action or state[3]-2==action):
            return -3,1,newState
        reward=self.reward(newState,map)
        map.cleaned[newState[1],newState[0]]=1
        if(self.algorithme=='dp'):
            return reward,0.25,newState
        elif(self.algorithme=='ql'):
            return reward,1,newState
        elif(self.algorithme=="mc"):
            return reward,1,newState
    def reward(self,state,map):
        if(map.complete()):
            return 10
        if(map.cleaned[state[1],state[0]]==0):
            return 5
        return 0
