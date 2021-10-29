import ql
import mc
import dp
import robot
import simulator
from matplotlib import pyplot as plt 
def show(reward):
    plt.plot(reward)
    plt.show()
if __name__=="__main__":
    print("choose the algorithme: ql for q-learning, dp for dynamic programming, mc for monte carlo")
    algos=["ql","dp","mc"]
    algo=""
    while(True):
        algo=input()
        if(algo not in algos):
            print("please enter one of 'ql','dp','mc'")
        else:
            break
    print("Do you want to see the trace on the map?y/n(default)")
    show=input()
    if(show=="y"):
        show=True
    else:
        show=False

    room=robot.map(3,3)
    clean_robot=robot.state(10)
    
    if(algo=="ql"):
        ql_algo=ql.ql(room,clean_robot)
        ql_algo.ql(room,clean_robot)
        room.init()
        clean_robot.init()
        while(True):
            action=ql.next(ql_algo.q,clean_robot.getState())
            clean_robot.run(action,room)
            if(show):
                room.show(clean_robot.getState())
            if(clean_robot.end() or room.complete()):
                exit()
    elif(algo=="dp"):
        dp_algo = dp.dp(room,clean_robot)
        dp_algo.dp(room)
        policy=dp_algo.policy
        room.init()
        clean_robot.init()

        while(True):
            for i in policy:
                clean_robot.run(i,room)
                if(show):
                    room.show(clean_robot.getState())
                if(clean_robot.end() or room.complete()):
                    exit()
    else:
        mc_algo=mc.mc(room,clean_robot)
        mc_algo.mc(room,clean_robot)
        print(type(mc_algo.reward))
        room.init()
        clean_robot.init()
        while(True):
            action=next(mc_algo.q,clean_robot.getState())
            clean_robot.run(action,room)
            if(show):
                room.show(clean_robot.getState())
            if(clean_robot.end() or room.complete()):
                exit()
