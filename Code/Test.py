import numpy as np
import matplotlib.pyplot as plt
import random
import math
import os

class Particle:
    def __init__(self,isRan=True,x=0,y=0):
        if isRan:
            self.x = random.uniform(-2.5,2.5)
            self.y = random.uniform(-2.5,2.5)
        else:
            self.x = x
            self.y = y
        self.ux = 0
        self.uy = 0
        self.mass = 1
        self.force = np.zeros([1,2])
        self.dt = 0.0005

    def motion_equation(self):
        # print("Force :", self.force[0,0])
        self.x = self.x + (self.ux * self.dt) +( 0.5 * self.force[0,0] * (self.dt**2))
        self.ux = self.ux + self.force[0,0] * self.dt
        self.y = self.y + (self.uy * self.dt) + (0.5 * self.force[0, 1] * (self.dt**2))
        self.uy = self.uy + self.force[0, 1] * self.dt


class LJ:
    def __init__(self):
        #initialising constants
        pass

    def force_calculate(self, A, B , isWall=False):
        #finding LJ for two particles A,B
        L = 5
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
        # distance1 = np.sqrt((A.x - B.x+L)**2 + (A.y - B.y)**2)
        # distance2 = np.sqrt((A.x - B.x)**2 + (A.y - B.y + L)**2)
        # distance3= np.sqrt((A.x - B.x - L)**2 + (A.y - B.y)**2)
        # distance4 = np.sqrt((A.x - B.x)**2 + (A.y - B.y - L)**2)
        if self.getAdjList(distance):
            r_vector = np.empty([1, 2])
            r_vector[0, 0] = (A.x - B.x) / distance
            r_vector[0, 1] = (A.y - B.y) / distance
            force_LJ = 24 * (2 * distance**(-14) - distance**(-8)) * r_vector
            A.force = A.force + force_LJ
            if ~isWall:
                B.force = B.force - force_LJ

    def force_wall_calculate(self,A):
        L  = 5
        walls = []
        walls.append([Particle(False,p.x+L, p.y) for p in particleList])
        walls.append([Particle(False, p.x - L, p.y) for p in particleList])
        walls.append([Particle(False, p.x, p.y + L) for p in particleList])
        walls.append([Particle(False, p.x, p.y - L) for p in particleList])
        # for particle in particleList:
        #     p1 =
        for wall in walls:
            for particle in wall:
                self.force_calculate(A,particle,isWall=True)


    def set_force(self,particleList):
        for x in particleList:
            x.force = np.zeros([1,2])

    def getAdjList(self,distance,cutoff=100):
        if distance<cutoff:
            return True
        else:
            False





if __name__ =="__main__":
    def multi_plot(i):
        x = []
        y = []
        for p in particleList:
            x.append(p.x)
            y.append(p.y)
        fig = plt.figure()
        plt.plot(x,y,'ro')
        fig.savefig('movie/'+str(t)+'.tif')


    def printStatus():
        for p in particleList:
            print(p.x,p.y,p.ux,p.uy,p.force)
        print("\n")

    num_particle = 5
    time_end = 3000
    dt = 0
    LJ = LJ() # initializing the LJ utility object
    particleList = [Particle() for count in range(num_particle)] #list of particles
    printStatus()
    for t in range(0,time_end):
        print(t)
        LJ.set_force(particleList) #initially setting the net force to zero
        for i in range (num_particle):
            for j in range(i+1,num_particle):  #inefficient with o(n^3)
                LJ.force_calculate(particleList[i],particleList[j])
            LJ.force_wall_calculate(particleList[i])
            particleList[i].motion_equation()
       # printStatus()
        multi_plot(t)





    # FORCE = LJ.force_calculate(A,)
    # print(FORCE)

