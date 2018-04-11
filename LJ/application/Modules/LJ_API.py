import numpy as np
import random
import math
import os
import sys
import time
import datetime
import pickle
import json
import matplotlib.pyplot as plt


from LJ.application.Modules.Particle import Particle
from LJ.application.Modules.LJ import LJ
from LJ.application.Modules.Cell import Cell
from LJ.application.Modules.cellutils import CellUtils
from LJ.application.Modules.Grapher import Grapher
from LJ.application.Modules.stress import Stress

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
        print("dt" + str(self.server_params['dt']))
        for i in range(0, int(math.sqrt(n))):  # 1 <= i <= n/2
            for j in range(0, int(math.sqrt(n))):
                x = initial_min_step * i - (initial_l/2) + (initial_min_step/2)
                y = initial_min_step * j - (initial_l/2) + (initial_min_step / 2)
                particleList.append(Particle(count,False,x,y))
                count+=1
        return particleList

    def set_toggle(self,toggle_move,toggle_direction):
        if toggle_move == 1:
            return 0,toggle_direction
        if toggle_move == -1:
            return 0,toggle_direction
        if toggle_move == 0 and toggle_direction:
            return 1,not toggle_direction
        if toggle_move == 0 and not toggle_direction:
            return -1,not toggle_direction

    def run(self):
        num_particle = self.server_params['num_particles']
        time_end = self.server_params['time_end']
        print_every = self.grapher_params['print_every']
        distance = self.server_params['distance']
        isCellList = self.server_params['cellList']

        move_every = 0
        toggle_variable = [-1,0,1]
        toggle_move = 0
        toggle_direction = True


        stress = Stress(self.stress_params['k'],self.stress_params["rc"],self.stress_params["r0"])
        lj = LJ(num_particle)
        particleList =self.init(num_particle) #list of particles

        graph = Grapher(distance,isCellList)
        if isCellList:
            cellworker = CellUtils(distance)
            cellList = cellworker.init_cells(particleList)
            cellworker.print_cellList(cellList)
            cellworker.findTopLine(particleList)
            # input()
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


            # if (t+1) % move_every == 0:
            #     # print("Toggle_move : {} toggle_direction : {} move: 1".format(toggle_move,toggle_direction))
            #     for x in cellworker.topLine:
            #         if toggle_direction:
            #             print("Toggle_move : {} toggle_direction : {} move: 1".format(toggle_move,toggle_direction))
            #             particleList[x]._move(1.5)
            #         else:
            #             print("Toggle_move : {} toggle_direction : {} move: -1".format(toggle_move,toggle_direction))
            #             particleList[x]._move(-1.5)
            #     toggle_move,toggle_direction = self.set_toggle(toggle_move,toggle_direction)

            if (t+1) % print_every == 0 or t==0:
                d3_dic =list()
                for particle in particleList:
                    d3_dic.append({"no":particle.id,"x":particle.x,"y":particle.y,"z":particle.potential});
                d = json.dumps(d3_dic)
                yield d
                # requests.post("localhost:5000/run", data={'number': 12524, 'type': 'issue', 'action': 'show'})

                #https://stackoverflow.com/questions/31948285/display-data-streamed-from-a-flask-view-as-it-updates

                if isCellList:
                    graph.multi_plot(t+1,particleList,cellList)
                else:
                    graph.multi_plot(t+1,particleList)


        elapsed_time = time.time() - start_time
        sys.stdout.write("\n Elapsed time is {:.2f} seconds.".format(elapsed_time))
        sys.stdout.write("\n Time taken to create graphs is {:.2f} seconds.".format(graph.graph_time))
        # if (t+1) % print_every == 0:
        #     if isCellList:
        #         graph.multi_plot("Last",particleList,cellList,False)
        #     else:
        #         graph.multi_plot("Last",particleList)
