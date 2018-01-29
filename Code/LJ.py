import numpy as np
import Particle


class LJ:
    def __init__(self):
        #initialising constants
        pass

    def force_calculate(self, A, B , isWall=False):
        #finding LJ for two particles A,B
        L = 5
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
        if self.getAdjList(distance):
            r_vector = np.zeros([1, 2])
            r_vector[0, 0] = (A.x - B.x) / distance
            r_vector[0, 1] = (A.y - B.y) / distance
            Potential = 24 * (2 * distance**(-14) - distance**(-8)) * r_vector
            force_LJ = 24 * (2 * -14* distance ** (-15) + 8 * distance ** (-9)) * r_vector
            # if force_LJ[0,0] > 100 or force_LJ[0,1] > 100:
            #     print("Force is more than 100 for particle")
            A.force = A.force + force_LJ
            if ~isWall:
                B.force = B.force - force_LJ
            return  force_LJ

    def force_wall_calculate(self,A,particleList):
        #periodic boundary conditions
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



