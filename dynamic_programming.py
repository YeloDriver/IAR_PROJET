import numpy as np
import robot


class DP:

    def __init__(self):
        self.states = []  # all possible states
        self.values = []
        self.epsilon = 0.01  # The threshold used to stop the interations
        self.discounted_factor = 0.99

    """
    generate all the possible states
    """

    def get_all_states(self): 
        #遍历电池、机器人当前位置、当前状态组成所有的状态列表
        for battery in range(robot.BATTERY+1):
            for pos_x in range(robot.MAPSIZE_X):
                for pos_y in range(robot.MAPSIZE_Y):
                    for robot_state in robot.STATE:
                        state = {
                            "robot_pos": (pos_x,pos_y),
                            "battery": battery,
                            "robot_action": robot_state, 
                        }
                        self.states.append(state)


    def get_infinite_norme(self, values, values_prime):
        return np.linalg.norm(abs(np.subtract(values,values_prime)), np.inf)

    def find_index_of_new_state(self, new_state):
        for i in range(len(self.states)):
            if new_state == self.states[i]:
                return i
            else:
                print("error : new state",new_state, " not in states list")
                return None
        
    def best_perf(self, q_values):
        indMax = 0
        valueMax = 0
        for i, v in enumerate(q_values):
            if v > valueMax:
                valueMax = v
                indMax = i

        return indMax, valueMax

    def dp(self):
        sim = simulator() #todo: 创建simulator
        self.get_all_states() #获取所有的状态
 
        #初始化value和上一轮的value
        value = [100.0 for _ in range(self.states)]
        value_prime = [-100.0 for _ in range(self.states)]

        #结束条件
        while self.get_infinite_norme(value,value_prime) >= self.epsilon:
            policy = [] #初始化机器人运行轨迹的数组

            value_prime = value 

            #遍历所有的状态
            for state_ind, state in enumerate(self.states):
                q_values = [0.0 for _ in range(4)] #初始化q值列表，长度为机器人的action

                #遍历全部action
                for action_ind, action in enumerate(robot.ACTION):
                    reward, probability, new_state = sim.simulate(state, action) #导入当前状态和动作，模拟下一步的情况，返还reward、可能性、下一状态
                    q_values[action_ind] = reward #将执行动作后的价值赋予q值

                    #可能会出现下一状态不存在或者可能性为0的情况
                    if new_state and (probability > 0):
                        new_state_ind = find_index_of_new_state(new_state) #查找下一状态在所有状态中的index
                        if new_state_ind is None: #有可能会不存在所有状态中？
                            break
                        q_values[action_ind] += self.discounted_factor * probability * value_prime[new_state_ind] #对q值进行调整

                # 将当前状态下，最优情况的动作保存进policy，最优q值保存进value数组里
                best_action, value[state_ind] = best_perf(q_values)
                policy.append(best_action)

        return policy
                

if __name__ == "__main__":  # simulator写好后理论上直接跑这个可以进行测试

    dp = DP()
    # dp.get_all_states()
    # print(dp.states)
    # print(dp.get_infinite_norme([1.1,1.2,1.3],[0.2,0.8,0.9]))
    policy = dp.dp()
    m = robot.map(10,10)
    m.wall_test()
    r = robot()
    while(True):
        for i in policy:
            m.showRobot(r, i)
            m.show()

