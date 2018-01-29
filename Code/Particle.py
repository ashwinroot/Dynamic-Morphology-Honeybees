import math
import random
import numpy as np

class Particle:
    def __init__(self,isRan=True,x=0,y=0, num_particle=9):
        self.lattice = {"size" :math.sqrt(num_particle),"half":num_particle/2}
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
        self.dt = 0.000005

    def motion_equation(self):
        #Equations of motion
        self.x = self.x + (self.ux * self.dt) +( 0.5 * self.force[0,0] * (self.dt**2))
        self.ux = self.ux + self.force[0,0] * self.dt
        self.y = self.y + (self.uy * self.dt) + (0.5 * self.force[0, 1] * (self.dt**2))
        self.uy = self.uy + self.force[0, 1] * self.dt
        # If the particle goes beyond the wall, readjust by the lattice
        if self.x > self.lattice["size"]:
            self.x = (self.x - (self.lattice["size"]))
            self.ux = -self.ux
        if self.x < 0:
            self.x = -self.x
            self.ux = -self.ux
        if self.y > self.lattice["size"]:
            self.y = self.y - self.lattice["size"]
            self.uy = -self.uy
        if self.y < 0:
            self.y = -(self.y)
            self.uy = -self.uy