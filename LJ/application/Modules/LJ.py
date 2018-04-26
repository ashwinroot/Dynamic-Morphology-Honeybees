import numpy as np
from LJ.application.Modules.Particle import Particle


class LJ:
    def __init__(self,cutoff,epsilon,dimension="2d"):
        self.cutoff = cutoff
        self.epsilon = epsilon
        self.dimension = dimension
        # self.L= 1.2 * 1.122 * np.sqrt(num_particle) #must be using number of particles



    def force_calculate(self, A, B , isWall=False):
        #finding LJ for two particles A,B
        if self.dimension=="3d":
            self.force_calculate_3d(A,B)
            return

        epsilon= self.epsilon
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
        if self.getAdjList(distance):
            r_vector = np.zeros([1, 2])
            r_vector[0, 0] = (B.x - A.x)
            r_vector[0, 1] = (B.y - A.y)

            if ~isWall:
                force_LJ = 24*epsilon*(2*distance**-14 - distance**-8) * r_vector
                A.force = A.force - force_LJ
                B.force = B.force + force_LJ
                A.potential += np.sum(A.force * r_vector)
            else:
                if distance > 0:
                    force_LJ = 24  * (-distance ** -8) * r_vector
                    A.force = A.force - force_LJ
            return  force_LJ

    #
    # def force_wall_calculate(self,A,particleList):
    #     walls = []
    #     walls.append(Particle(False, self.L / 2, A.y))
    #     walls.append(Particle(False,-self.L/2,A.y))
    #     walls.append(Particle(False, A.x, self.L/2))
    #     walls.append(Particle(False, A.x, -self.L/2))
    #     for particle in walls:
    #         self.force_calculate(A,particle,isWall=True)


    def force_calculate_3d(self, A, B , isWall=False):
        #finding LJ for two particles A,B

        epsilon= self.epsilon
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2 + (A.z-B.z)**2)
        if self.getAdjList(distance):
            r_vector = np.zeros([1, 3])
            r_vector[0, 0] = (B.x - A.x)
            r_vector[0, 1] = (B.y - A.y)
            r_vector[0, 2] = (B.z - A.z)

            if ~isWall:
                force_LJ = 24*epsilon*(2*distance**-14 - distance**-8) * r_vector
                A.force = A.force - force_LJ
                B.force = B.force + force_LJ
                A.potential += np.sum(A.force * r_vector)
            else:
                if distance > 0:
                    force_LJ = 24  * (-distance ** -8) * r_vector
                    A.force = A.force - force_LJ
            return  force_LJ

    def set_force(self,particleList):
        for x in particleList:
            if self.dimension=="2d":
                x.force = np.zeros([1,2])
            else:
                x.force = np.zeros([1,3])
            x.potential = 0

    def getAdjList(self,distance):
        if distance<self.cutoff:
            return True
        else:
            return False
