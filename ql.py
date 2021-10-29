import robot
import simulator
import numpy as np
from random import randint,random
from matplotlib import pyplot as plt 
def show(reward):
    plt.plot(reward)
    plt.title("reward of each episode")
    plt.show()
class ql:
    def __init__(self,map,robot):
        self.x=map.x
        self.y=map.y
        self.q=np.zeros((map.x,map.y,robot.batteryMax+1,4,4))
        self.q_prime=np.zeros((map.x,map.y,robot.batteryMax+1,4,4))
        self.episode=1000
        #the influence of the futur state
        self.gamma=0
        #learnging rate
        self.rate=0.1
        #epsilon-greedy
        self.greedy=0.9
        self.reward=[]

    
    def ql(self,map,clean_robot):
        simu=simulator.simulator("ql")
        map=robot.map(self.x,self.y)
        #i have writed the condition with the convergence of the qTable,but it cost too much time
        #while((q-q1).any>self.greedy)
        for _ in range(self.episode):
            r=0
            self.q1=self.q.copy()
            map.init()
            clean_robot.init()
            state=clean_robot.getState()
            while(not clean_robot.end() and not map.complete()):
                if(random()>self.greedy):
                    action=randint(0,3)
                else:
                    action=next(self.q1,state)
                reward,_,newState=simu.simulate(state,action,map)
                self.q[state[0]][state[1]][state[2]][state[3]][action]=(reward+self.gamma*self.q[newState[0]][newState[1]][newState[2]][state[3]].max())*self.rate+(1-self.rate)*self.q[state[0]][state[1]][state[2]][state[3]][action]
                state=newState
                clean_robot.set(state)
                r+=reward
            self.reward.append(r)
        show(self.reward)
# get the next action with the qTable
def next(qTable,state):
        actions=[]
        for i in range(4):
            actions.append(qTable[state[0]][state[1]][state[2]][state[3]][i])
        min=-100
        next=0
        same_value=[0]
        for index,value in enumerate(actions):
            if(value>min):
                next=index
                min=value
                same_value=[]
                same_value.append(index)
            elif(value==min):
                same_value.append(index)
        if(len(same_value)==1):
            return next
        else:
            return same_value[randint(0,len(same_value)-1)]

if __name__=="__main__":
    room=robot.map(10,10)
    clean_robot=robot.state(100)
    q=ql(room,clean_robot)
    q.ql(room,clean_robot)
    room.init()
    clean_robot.init()
    while(True):
        action=next(q.q,clean_robot.getState())
        clean_robot.run(action,room)
        room.show(clean_robot.getState())
        if(clean_robot.end() or room.complete()):
            exit()
