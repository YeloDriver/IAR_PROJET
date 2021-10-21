import numpy as np 
from matplotlib import pyplot as plt 
from random import randint
class robot:
    def __init__(self):
        self.posX=0
        self.posY=0
        self.action=0
        self.battery=50
        #state 1:active 2:wait 3:return
        self.state=1
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
    def back(self):
        if(self.action==0):
            self.posY-=1
        if(self.action==1):
            self.posX-=1
        if(self.action==2):
            self.posY+=1
        if(self.action==3):
            self.posX+=1
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
    def wall_test(self):
        self.map[55:100,40]=3
        self.map[0:35,55]=3
        self.map[50,60:100]=3
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

m=map(100,100)
m.wall_test()
r=robot()
while(True):
    m.showRobot(r,randint(0,3))
    #delete if don't want to show the graph
    m.show()
