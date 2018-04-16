import numpy as np
from LJ.application.Modules.Particle import Particle

class Stress:
    def __init__(self,K,rc,r0=1.12):
        self.K = K
        self.rc = rc
        self.r0 = r0
        print("Self.rc" +str(self.rc))


    def force_calculate(self,A,B):
        distance = np.sqrt((A.x - B.x)**2 + (A.y - B.y)**2)
        if distance<self.rc:
            r_vector = np.zeros([1, 2])
            diff = distance - self.r0
            r_vector[0, 0] = (B.x - A.x) / distance
            r_vector[0, 1] = (B.y - A.y) /distance
            A.spring_interacted.append(B.id)
            force =  self.K * diff * r_vector
            A.force = A.force + force
            B.force = B.force - force
        else:
            # print("\t The particles "+str(A.id) +" and "+ str(B.id) + "is "+ str(distance) +" far away.")
            force = np.zeros([1, 2])
