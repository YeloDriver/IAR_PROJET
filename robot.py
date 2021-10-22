import numpy as np 
from matplotlib import pyplot as plt 
from random import randint

MAPSIZE_X = 10
MAPSIZE_Y = 10
BATTERY = 100
#state 1:active 2:wait 3:return
STATE = [1,2,3]
ACTION = [0,1,2,3]

class robot:
    def __init__(self):
        self.posX=0
        self.posY=0
        self.action=0
        self.battery = BATTERY
        self.state=1
    #robot run one step in a period and a period cost 1 battery
    def run(self,action):
        self.action=action
        if(self.action==0):
            self.posY+=1
        if(self.action==1):
            self.posX+=1
        if(self.action==2):
            self.posY-=1
        if(self.action==3):
            self.posX-=1
    #if there is a wall or a frontier before the robot, the last action will not happen
    def back(self):
        if(self.action==0):
            self.posY-=1
        if(self.action==1):
            self.posX-=1
        if(self.action==2):
            self.posY+=1
        if(self.action==3):
            self.posX+=1
    #out of battery
    def end(self):
        if(self.battery==0):
            exit()

class map:
    #create a new map
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.state=np.zeros((x,y))
        self.map=np.zeros((x,y))
    #show the map. If it's used after showRobot(), the robot will also shown in the map
    def show(self):
        plt.cla()
        plt.imshow(self.state,origin="lower")
        plt.pause(0.1)
    #create x random walls on the map （x is the number） and all the walls starts from the frontier
    def wall(self,number):
        for i in range(number):
            frontier=randint(0,3)
            if(frontier==0):
                self.map[randint(0,self.y-1):self.y,randint(0,self.x-1)]=3
            if(frontier==1):
                self.map[randint(0,self.y),randint(0,self.x):self.x]=3
            if(frontier==2):
                self.map[0:randint(0,self.y-1),randint(0,self.x-1)]=3
            if(frontier==3):
                self.map[randint(0,self.y-1),0:randint(0,self.x-1)]=3
    #wall for test which will not change
    def wall_test(self):
        self.map[5:10,4]=3
        self.map[0:3,5]=3
        self.map[5,6:10]=3
    #show the robot on the map    
    def showRobot(self,robot,action):
        robot.run(action)
        #robot touch the frontier or the wall
        if(robot.posX>=self.x or robot.posY>=self.y or robot.posX<0 or robot.posY<0 or self.map[robot.posY,robot.posX]==3):
            robot.back()
        else:
            self.map[robot.posY,robot.posX]=1
            self.state=self.map.copy()
            self.state[robot.posY,robot.posX]=2
            robot.battery-=1
            robot.end()


if __name__ == "__main__":
    m = map(MAPSIZE_X, MAPSIZE_Y)
    m.wall_test()
    r=robot()
    while(True):
        m.showRobot(r,randint(0,3))
        #delete if don't want to show the graph
        m.show()
