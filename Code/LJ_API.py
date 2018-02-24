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
from Cell import Cell
from cellutils import CellUtils
from Grapher import Grapher

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
    count =0
    for i in range(0, int(math.sqrt(n))):  # 1 <= i <= n/2
        for j in range(0, int(math.sqrt(n))):
            x = initial_min_step * i - (initial_l/2) + (initial_min_step/2)
            y = initial_min_step * j - (initial_l/2) + (initial_min_step / 2)
            particleList.append(Particle(count,False,x,y))
            count+=1
    return particleList

def run():
    num_particle = 100
    time_end = 3000
    print_every = 100
    lj = LJ(num_particle) # initializing the LJ utility object
    cellworker =CellUtils()
    graph = Grapher()
    particleList =init(num_particle) #list of particles
    cellList = cellworker.init_cells(particleList,1.5)
    cellworker.print_cellList(cellList)

    start_time = time.time()

    graph.multi_plot(-1,particleList,cellList)


    for t in range(0,time_end):

        #printing the time down
        sys.stdout.write("\r Time elapsed : {:.2f} seconds \t Iteration: {}".format(time.time()-start_time,t+1))
        sys.stdout.flush()

        lj.set_force(particleList) #initially setting the net force to zero

        for i in range (num_particle):
            for j in range(i+1,num_particle):  #inefficient with o(n^3)
                lj.force_calculate(particleList[i],particleList[j])

        for i in range(num_particle):
            particleList[i].motion_equation()

        if (t+1) % print_every == 0:
            graph.multi_plot(t+1,particleList,cellList)


    elapsed_time = time.time() - start_time
    sys.stdout.write("\n Elapsed time is {:.2f} seconds.".format(elapsed_time))
    sys.stdout.write("\n Time taken to create graphs is {:.2f} seconds.".format(graph.graph_time))

run()
