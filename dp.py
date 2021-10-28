import robot
import simulator
import numpy as np
from random import randint

class dp:
    def __init__(self,map,robot):
        self.x=map.x
        self.y=map.y
        self.batteryMax=robot.batteryMax
        self.states=[]
        self.policy=[]
        self.epsilon = 0.01  # The threshold used to stop the interations
        self.discounted_factor = 0.99
    
    def getAllState(self):
        for action in range(4):
            for battery in range(self.batteryMax):
                for y in range(self.y):
                    for x in range(self.x):
                        state=[x,y,battery,action]
                        self.states.append(state)
    def best_perf(self, q_values):
        indMax = 0
        valueMax = 0
        for i, v in enumerate(q_values):
            if v > valueMax:
                valueMax = v
                indMax = i

        return indMax, valueMax
    def dp(self,map):
        simu=simulator.simulator("dp")
        self.getAllState()
        value = [100.0 for _ in range(len(self.states))]
        value_prime = [-100.0 for _ in range(len(self.states))]
        #之后改成norme infini
        for i in range(1000):
            policy=[]
            value_prime=value
            for state_ind,state in enumerate(self.states):
                q_values=[0 for _ in range(4)]
                for action in range(4):
                    reward, probability, newState = simu.simulate(state, action,map)
                    q_values[action] = reward

                    if newState and (probability > 0):
                        newStateInd=self.states.index(newState)
                        if newStateInd is None: #有可能会不存在所有状态中？
                            break
                        q_values[action] += self.discounted_factor * probability * value_prime[newStateInd]
                best_action, value[state_ind] = self.best_perf(q_values)
                policy.append(best_action)
        self.policy=policy

if __name__ == "__main__":  # simulator写好后理论上直接跑这个可以进行测试

        
    room=robot.map(3,3)
    clean_robot=robot.state(10)
    dp = dp(room,clean_robot)
    dp.dp(room)
    policy=dp.policy
    room.init()
    clean_robot.init()

    while(True):
        for i in policy:
            clean_robot.run(i,room)
            room.show(clean_robot.getState())
            if(clean_robot.end() or room.complete()):
                exit()
