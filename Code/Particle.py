import math
import random
import numpy as np

class Particle:
    def __init__(self,isRan=True,x=0,y=0, num_particle=100):
        self.lattice = {"size" :math.sqrt(num_particle)+2.5,"half":num_particle/2}
        if isRan:
            self.x = random.uniform(-self.lattice["size"]/2,self.lattice["size"]/2)
            self.y = random.uniform(-self.lattice["size"]/2,self.lattice["size"]/2)
        else:
            self.x = x
            self.y = y
        self.ux = 0
        self.uy = 0
        self.mass = 1
        self.force = np.zeros([1,2])
        self.dt =0.0005

    def motion_equation(self):
        #Equations of motion
        # self.x = self.x + (self.ux * self.dt) +( 0.5 * self.force[0,0] * (self.dt**2))
        # self.ux = self.ux + self.force[0,0] * self.dt
        # self.y = self.y + (self.uy * self.dt) + (0.5 * self.force[0, 1] * (self.dt**2))
        # self.uy = self.uy + self.force[0, 1] * self.dt
        self.x = self.x + self.dt *self.force[0,0]
        self.y = self.y + self.dt *self.force[0,1]