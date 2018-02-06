import numpy as np
from Particle import Particle


class LJ:
    def __init__(self):
        self.cutoff = 2.5
        self.L= 1.2 * 1.122 * np.sqrt(100) #must be using number of particles



    def force_calculate(self, A, B , isWall=False):
        #finding LJ for two particles A,B
        epsilon= 5
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
        if self.getAdjList(distance):
            r_vector = np.zeros([1, 2])
            r_vector[0, 0] = (B.x - A.x)
            r_vector[0, 1] = (B.y - A.y)

            if ~isWall:
                force_LJ = 24*epsilon*(2*distance**-14 - distance**-8) * r_vector
                # force_LJ = 24*epsilon*(-28*(distance**-13) +8*(distance**-7) ) *r_vector
                A.force = A.force - force_LJ
                B.force = B.force + force_LJ
            else:
                if distance > 0:
                    force_LJ = 24  * (-distance ** -8) * r_vector
                    A.force = A.force - force_LJ
            return  force_LJ


    def force_wall_calculate(self,A,particleList):
        walls = []
        walls.append(Particle(False, self.L / 2, A.y))
        walls.append(Particle(False,-self.L/2,A.y))
        walls.append(Particle(False, A.x, self.L/2))
        walls.append(Particle(False, A.x, -self.L/2))
        for particle in walls:
            self.force_calculate(A,particle,isWall=True)



    def set_force(self,particleList):
        for x in particleList:
            x.force = np.zeros([1,2])

    def getAdjList(self,distance):
        if distance<self.cutoff:
            return True
        else:
            False



