import robot
import simulator
import numpy as np
from random import randint

class mc:
    def __init__(self,map,robot):
        self.x=map.x
        self.y=map.y
        self.batteryMax=robot.batteryMax
        self.q=np.zeros(map.x*map.y*(robot.batteryMax+1)*4)
        self.returns={}
        self.episode=1000
    def stateToKey(self,newState):
        return newState[0]*self.y*(self.batteryMax+1)*4+newState[1]*(self.batteryMax+1)*4+newState[2]*4+newState[3]
    
    def keyToState(self,key):
        x=key//(self.y*(self.batteryMax+1)*4)
        y=(key-x*(self.y*(self.batteryMax+1)*4))//((self.batteryMax+1)*4)
        battery=(key-x*(self.y*(self.batteryMax+1)*4)-y*((self.batteryMax+1)*4))//4
        last_action=key-x*(self.y*(self.batteryMax+1)*4)-y*((self.batteryMax+1)*4)-battery*4
        return [x,y,battery,last_action]

    def mc(self,map,robot):
        simu=simulator.simulator("mc")
        stateKey=self.batteryMax*4
        state=robot.getState()
        for i in range(self.episode):
            map.init()
            robot.init()
            state=robot.getState()
            while(not robot.end() or not map.complete()):
                stateKey=self.stateToKey(state)
                action=randint(0,4)
                reward, probability, newState = simu.simulate(state, action,map)
                if(not stateKey in self.returns.keys()):
                    self.returns[stateKey]=0
                for key in self.returns.keys(): 
                    self.returns[key] += reward
                newStateKey=self.stateToKey(newState)
                state=newState
            for key in self.returns.keys():
                self.q[key] = (self.q[key] * (i - 1) + self.returns[key]) / i
    def next(self,state):
        return np.argmax(self.q[state[0]][state[1]][state[2]][state[3]])

if __name__=="__main__":
    room=robot.map(10,10)
    clean_robot=robot.state(100)
    q=mc(room,clean_robot)
    q.mc(room,clean_robot)
    room.init()
    clean_robot.init()
    while(True):
        action=next(q.q,clean_robot.getState())
        print(action)
        clean_robot.run(action,room)
        room.show(clean_robot.getState())
        if(clean_robot.end() or room.complete()):
            exit()
