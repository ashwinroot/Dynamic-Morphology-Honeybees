import math
import random
import sys
import numpy as np

class Particle:
    def __init__(self,id,isRan=True,x=0,y=0,dt=0.0005, num_particle=100):
        self.id = id
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
        self.potential = 0
        self.cell = None
        self.dt = 0.0005
        self.interacted = list()

    def motion_equation(self):
        #Equations of motion
        self.x = self.x + self.dt *self.force[0,0]
        self.y = self.y + self.dt *self.force[0,1]

    def status(self):
        sys.stdout.write("\n Particle : {} ({},{}), Force: [{},{}]".format(self.id,self.x,self.y,self.force[0,0],self.force[0,1]))
