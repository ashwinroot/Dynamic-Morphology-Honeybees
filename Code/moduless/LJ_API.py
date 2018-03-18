import numpy as np
import matplotlib.pyplot as plt
import random
import math
import os
import sys
import time
import datetime
import pickle

from moduless.Particle import Particle
from moduless.LJ import LJ
from moduless.Cell import Cell
from moduless.cellutils import CellUtils
from moduless.Grapher import Grapher
from moduless.stress import Stress

class API:
    def __init__(self,SERVER_PARAMS,GRAPHER_PARAMS,STRESS_PARAM):
        self.server_params =SERVER_PARAMS
        self.grapher_params = GRAPHER_PARAMS
        self.stress_params = STRESS_PARAM

    def init(self,n):
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

    def run(self):
        num_particle = self.server_params['num_particles']
        time_end = self.server_params['time_end']
        print_every = self.grapher_params['print_every']
        distance = self.server_params['distance']
        isCellList = self.server_params['cellList']


        stress = Stress(self.stress_params["k"],self.stress_params["rc"],self.stress_params["r0"])
        lj = LJ(num_particle)
        particleList =self.init(num_particle) #list of particles

        graph = Grapher(distance,isCellList)
        if isCellList:
            cellworker = CellUtils(distance)
            cellList = cellworker.init_cells(particleList)
            cellworker.print_cellList(cellList)
            input()
            cellworker.init_allocation(cellList=cellList,particleList=particleList)

        # cellworker.print_cellList(cellList)
        start_time = time.time()

        if isCellList:
            graph.multi_plot(-1,particleList,cellList)
        else:
            graph.multi_plot(-1,particleList)


        for t in range(0,time_end):
            # input("")
            #printing the time down
            sys.stdout.write("\r Time elapsed : {:.2f} seconds \t Iteration: {}".format(time.time()-start_time,t+1))
            sys.stdout.flush()
            if isCellList:
                cellworker.init_allocation(cellList=cellList,particleList=particleList)
            lj.set_force(particleList) #initially setting the net force to zero

            if isCellList:
                for i,cell in enumerate(cellList):
                    adjacent  = cell.getAdjacentParticles()
                    # sys.stdout.write("\n Cell id : {} Adjacent Particle count: {} ".format(cell.id,len(adjacent)))
                    # input("")
                    for particlei in list(cell.particleList.values()):
                        # print(particlei.interacted)
                        for particlej in adjacent:
                            if particlej.id not in particlei.interacted:
                                if particlei.id != particlej.id:
                                    # sys.stdout.write("\n \t {} interacting with {}".format(particlei.id, particlej.id))
                                    lj.force_calculate(particlei,particlej)
                                    stress.force_calculate(particlei,particlej)
                                    particlei.interacted.append(particlej.id)
                                    particlej.interacted.append(particlei.id)
            else:
                for i in range (num_particle):
                    for j in range(i+1,num_particle):  #inefficient with o(n^3)
                        lj.force_calculate(particleList[i],particleList[j])
                        stress.force_calculate(particleList[i],particleList[j])

            for i in range(num_particle):
                particleList[i].motion_equation()

            if (t+1) % print_every == 0:
                if isCellList:
                    graph.multi_plot(t+1,particleList,cellList)
                else:
                    graph.multi_plot(t+1,particleList)


        elapsed_time = time.time() - start_time
        sys.stdout.write("\n Elapsed time is {:.2f} seconds.".format(elapsed_time))
        sys.stdout.write("\n Time taken to create graphs is {:.2f} seconds.".format(graph.graph_time))
        if (t+1) % print_every == 0:
            if isCellList:
                graph.multi_plot("Last",particleList,cellList,False)
            else:
                graph.multi_plot("Last",particleList)
