import numpy as np
import matplotlib.pyplot as plt
import random
import math
import os
import sys
import time
import datetime
import pickle

from Particle import Particle
from LJ import LJ

if __name__ =="__main__":
    timestr = time.strftime("%Y%m%d-%H%M%S")
    save_path = "output/" + timestr

    def multi_plot(i):
        if not os.path.exists(save_path):
            sys.stdout.write("\n Created the file {}".format(save_path))
            os.makedirs(save_path)

        x ,y = [] , []

        for count,p in enumerate(particleList):
            x.append(p.x)
            y.append(p.y)

        with open('dump.pkl','a+b') as f:
            pickle.dump(particleList,f)

        # sys.stdout.write("\r Graph drawing for {}".format(i))
        # sys.stdout.flush()

        fig = plt.figure()
        plt.title("Plotting "+str(i))
        ax = plt.gca()
        ax.set_ylim([-1,4])
        ax.set_xlim([-1,4])
        plt.plot(x,y,'ro')
        fig.savefig(save_path+"/"+str(i)+'.jpg')

    # 9 particles
    #
    def init_particles(n=9):
        a= 1.12
        particleList = []
        for i in range (0,int(math.sqrt(n))): # 1 <= i <= n/2
            for j in range(0,int(math.sqrt(n))):
                noise = random.uniform(-0.2,0.2)
                particleList.append(Particle(False,a*i+noise,a*j+noise))
        return particleList



    def printStatus():
        for count, p in enumerate(particleList):
            sys.stdout.write("\r Particle: {}\n x: {:.2f} y: {:.2f} ux: {:.2f} uy: {:.2f} NetForce: [{:.2f},{:.2f}]\n".format(count,p.x,p.y,p.ux,p.uy,p.force[0][0],p.force[0][1]))
            sys.stdout.flush()
        print("\n")

    num_particle = 9
    time_end = 3000
    dt = 0
    LJ = LJ() # initializing the LJ utility object
    particleList =init_particles(num_particle) #list of particles
    print("Particle list",particleList)
    #initialising the particles:

    printStatus()
    start_time = time.time()
    multi_plot(-1)

    for t in range(0,time_end):

        #printing the time down
        sys.stdout.write("\rTime elapsed : {:.2f} seconds \t Iteration: {}".format(time.time()-start_time,t+1))
        sys.stdout.flush()

        LJ.set_force(particleList) #initially setting the net force to zero
        for i in range (num_particle):
            for j in range(i+1,num_particle):  #inefficient with o(n^3)
                force = LJ.force_calculate(particleList[i],particleList[j])
                # sys.stdout.write("\r Iteration {}: {} interacting {} with {}".format(t,i,j,force))
                # time.sleep(1)
                # sys.stdout.flush()
            # LJ.force_wall_calculate(particleList[i],particleList)
        for i in range(num_particle):
            particleList[i].motion_equation()
            #printStatus()
        # multi_plot(t)


    elapsed_time = time.time() - start_time






    # FORCE = LJ.force_calculate(A,)
    # print(FORCE)
