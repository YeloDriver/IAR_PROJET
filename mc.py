import robot
import simulator
import numpy as np
from random import randint,random
from matplotlib import pyplot as plt 
def show(reward):
    plt.plot(reward)
    plt.title("reward of each episode")
    plt.show()
class mc:
    def __init__(self,map,robot):
        self.x=map.x
        self.y=map.y
        self.batteryMax=robot.batteryMax
        self.q=np.zeros(map.x*map.y*(robot.batteryMax+1)*4)
        self.q1=self.q.copy()
        self.returns={}
        self.episode=1000
        self.reward=[]
        self.epsilon=0.9
        self.START_EPSILON_DECAY = 1
        self.END_EPSILON_DECAY = self.episode // 2
        self.epsilon_decay_value = self.epsilon / (self.END_EPSILON_DECAY - self.START_EPSILON_DECAY)
    def stateToKey(self,newState):
        return newState[0]*self.y*(self.batteryMax+1)*4+newState[1]*(self.batteryMax+1)*4+newState[2]*4+newState[3]
    
    def keyToState(self,key):
        x=key//(self.y*(self.batteryMax+1)*4)
        y=(key-x*(self.y*(self.batteryMax+1)*4))//((self.batteryMax+1)*4)
        battery=(key-x*(self.y*(self.batteryMax+1)*4)-y*((self.batteryMax+1)*4))//4
        last_action=key-x*(self.y*(self.batteryMax+1)*4)-y*((self.batteryMax+1)*4)-battery*4
        return [x,y,battery,last_action]

    def mc(self,map,clean_robot):
        simu=simulator.simulator("mc")
        stateKey=self.batteryMax*4
        state=clean_robot.getState()
        #while((q-q1).any>self.greedy)
        for i in range(self.episode):
            self.q1=self.q.copy()
            r=0
            map.init()
            clean_robot.init()
            state=clean_robot.getState()
            stateKey=self.batteryMax*4
            while(not clean_robot.end() and not map.complete()):
                #print(clean_robot.getState())
                stateKey=self.stateToKey(state)
                if(random()>self.epsilon):
                    action=randint(0,3)
                else:
                    action=self.next(state)
                reward, probability, newState = simu.simulate(state, action,map)
                #print(newState)
                r+=reward
                if(not stateKey in self.returns.keys()):
                    self.returns[stateKey]=0
                for key in self.returns.keys(): 
                    self.returns[key] += reward
                newStateKey=self.stateToKey(newState)
                state=newState
                clean_robot.set(state)
            for key in self.returns.keys():
                self.q[key] = (self.q[key] * (i ) + self.returns[key]) / (i+1)
            if self.END_EPSILON_DECAY >= i >= self.START_EPSILON_DECAY:
                self.epsilon -= self.epsilon_decay_value
            self.reward.append(r)
        show(self.reward)
    def next(self,state):
        next=state[0]*self.y*(self.batteryMax+1)*4+state[1]*(self.batteryMax+1)*4+state[2]*4
        return np.argmax(self.q[next:next+4])

if __name__=="__main__":
    room=robot.map(3,3)
    clean_robot=robot.state(10)
    q=mc(room,clean_robot)
    q.mc(room,clean_robot)
    print(q.q)
    room.init()
    clean_robot.init()
    while(True):
        action=q.next(clean_robot.getState())
        clean_robot.run(action,room)
        room.show(clean_robot.getState())
        if(clean_robot.end() or room.complete()):
            exit()
