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
    timestr = time.strftime("%YY%mM%dD-%HH%MM%SS")
    save_path = "output/" + timestr

    def multi_plot(i):
        tic1 = time.time()
        if not os.path.exists(save_path):
            sys.stdout.write("\n Created the file {}".format(save_path))
            os.makedirs(save_path)

        x ,y = [] , []

        for count,p in enumerate(particleList):
            x.append(p.x)
            y.append(p.y)

        with open(save_path+'/indump.pkl','a+b') as f:
            pickle.dump(particleList,f)

        # sys.stdout.write("\r Graph drawing for {}".format(i))
        # sys.stdout.flush()


        fig = plt.figure()
        plt.title("Plotting "+str(i))
        ax = plt.gca()
        # ax.set_ylim([-100,100])
        # ax.set_xlim([-100,100])
        plt.plot(x,y,'ro')
        fig.savefig(save_path+"/"+str(i)+'.jpg')
        tic2 = time.time()
        return (tic2-tic1)

    # 9 particles
    #
    # def init_particles(n=9):
    #     a= 2.5
    #     particleList = []
    #     for i in range (0,int(math.sqrt(n))): # 1 <= i <= n/2
    #         for j in range(0,int(math.sqrt(n))):
    #             noise = random.uniform(-0.5,0.5)
    #             noise = 0
    #             particleList.append(Particle(False,a*i+noise,a*j+noise))
    #     return particleList

    def init(n):
        particleList = []
        particles_per_edge = np.ceil(np.sqrt(n))
        initial_min_step = 1.2 * 1.122
        initial_l = particles_per_edge * initial_min_step
        for i in range(0, int(math.sqrt(n))):  # 1 <= i <= n/2
            for j in range(0, int(math.sqrt(n))):
                x = initial_min_step * i - (initial_l/2) + (initial_min_step/2)
                y = initial_min_step * j - (initial_l/2) + (initial_min_step / 2)
                particleList.append(Particle(False,x,y))
        return particleList



    def printStatus():
        for count, p in enumerate(particleList):
            sys.stdout.write("\r Particle: {}\n x: {:.2f} y: {:.2f} ux: {:.2f} uy: {:.2f} NetForce: [{:.2f},{:.2f}]\n".format(count,p.x,p.y,p.ux,p.uy,p.force[0][0],p.force[0][1]))
            sys.stdout.flush()
        print("\n")

    num_particle = 100
    time_end = 3000
    print_every = 100
    LJ = LJ() # initializing the LJ utility object
    particleList =init(num_particle) #list of particles
    # print("Particle list",particleList)


    time_graph = 0
    start_time = time.time()
    multi_plot(-1)


    for t in range(0,time_end):

        #printing the time down
        sys.stdout.write("\rTime elapsed : {:.2f} seconds \t Iteration: {}".format(time.time()-start_time,t+1))
        sys.stdout.flush()

        LJ.set_force(particleList) #initially setting the net force to zero


        for i in range (num_particle):
            for j in range(i+1,num_particle):  #inefficient with o(n^3)
                LJ.force_calculate(particleList[i],particleList[j])

            #LJ.force_wall_calculate(particleList[i],particleList)

        for i in range(num_particle):
            particleList[i].motion_equation()

        if t+1%print_every== 0:
            time_graph = time_graph + multi_plot(t)


    elapsed_time = time.time() - start_time
    sys.stdout.write("\n Elapsed time is {:.2f} seconds.".format(elapsed_time))
    sys.stdout.write("\n Time taken to create graphs is {:.2f} seconds.".format(time_graph))
