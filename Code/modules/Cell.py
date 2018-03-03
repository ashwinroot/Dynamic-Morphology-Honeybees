from Particle import Particle
from collections import defaultdict
import sys
import itertools

class Cell:
    def __init__(self,idx,x1,y1,x2,y2,l):
        self.id = idx
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.boundary = {"TOP":None,"LEFT":None,"RIGHT":None,"BOTTOM":None,"TOPRIGHT":None,"TOPLEFT":None,"BOTTOMRIGHT":None,"BOTTOMLEFT":None}
        self.particleList = defaultdict()
        self.count = 0
        self.l = l
        self.already_interacted = False

    def add_particle(self,A):
        self.particleList[A.id] = A
        self.count +=1

    def remove_particle(self,A):
        self.particleList.pop(A.id, None)
        self.count -= 1

    def check_if_present(self,A):
        if self.x1 >=A.x and A.x<=self.x2:
            if self.y1 >=A.y and A.y<=self.y2:
                return True
        return False

    def status(self):
        sys.stdout.write("\n ({},{}) to ({},{}) and has {} particles. ".format(self.x1,self.y1,self.x2,self.y2,self.count))


    def getAdjacentParticles(self):
        adjacentParticleList = list(self.particleList.values())
        for x in self.boundary:
            if self.boundary[x] != None:
                print("Getting values from " + x)
                adjacentParticleList = adjacentParticleList+ list(self.boundary[x].particleList.values())
        return adjacentParticleList
