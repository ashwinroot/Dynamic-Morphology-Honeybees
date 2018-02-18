from Particle import Particle
from collections import defaultdict

class Cell:
    def __init__(self,x1,y1,x2,y2,l):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.particleList = defaultdict()

    def add_particle(self,A):
        self.particleList[A.id] = A

    def remove_particle(self,A):
        self.particleList[A.id].remove()

    def check_if_present(self,A):
        if self.x1 >A.x and A.x<self.x2:
            if self.y1 >A.y and A.y<self.y2:
                return True
        return False