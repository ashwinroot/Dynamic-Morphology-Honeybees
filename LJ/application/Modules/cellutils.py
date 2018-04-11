from LJ.application.Modules.Cell import Cell
from LJ.application.Modules.Particle import Particle
import numpy as np
import sys

class CellUtils():
    def __init__(self,distance=1.5):
        self.bound = {"x1": None,"y1": None,"x2": None,"y2":None}
        self.distance = distance
        self.num_cell = 0

    def findCell(self,cellList,startx,starty,endx,endy):
        for i,cell in enumerate(cellList):
            # print(i)
            if cell.x1 ==startx and cell.y1 ==starty:
                # print("Found cell")
                # input()
                return cell
        return None

    def findTopLine(self,particleList):
        self.topLine = list()
        for particle in particleList:
            if particle.y == self.top_y:
                self.topLine.append(particle.id)

    def init_cells(self,particleList,distance=1.5):
        distance = self.distance
        print("\n Initialising cells")
        num_particles = particleList
        cellList = []
        b_x1,b_y1,b_x2,b_y2 = 0,0,0,0
        sqrt_distance = np.sqrt(2)* distance
        counter = "A"
        #getting the bounds of the system (#ask orit)
        for particle in particleList:
            if particle.x < b_x1:
                b_x1 = particle.x
            if particle.y < b_y1:
                b_y1 = particle.y
            if particle.x > b_x2:
                b_x2 = particle.x
            if particle.y > b_y2:
                b_y2 = particle.y


        self.bound["x1"] = b_x1 - 0.09
        self.bound["x2"] = b_x2 + 0.09
        self.bound["y1"] = b_y1 - 0.09
        self.bound["y2"] = b_y2 + 0.09

        self.top_y = b_y2


        print("\n Boundaries are "+ str(self.bound["x1"]) +str(self.bound["y1"]) +str(self.bound["x2"])   +  str(self.bound["y2"]))


        length = np.sqrt((self.bound["x1"] - self.bound["x1"]) ** 2 + (self.bound["y1"] - self.bound["y2"]) ** 2)
        self.num_cell = int(length / self.distance) +1

        # initialising the x,y s of cells
        for i in range(self.num_cell):
            for j in range(self.num_cell):
                cellList.append(Cell(counter,self.bound["x1"]+self.distance*i , self.bound["y1"]+self.distance*j, self.bound["x1"]+self.distance*(i+1),self.bound["y1"]+self.distance*(j+1),self.distance))
                counter = chr(ord(counter)+1) #incrementing ascii

        #ADJACENT CELL FILLING
        for i, cell in enumerate(cellList):
            # print(i)
            #find top
            cell.boundary["TOP"] = self.findCell(cellList,cell.x1,cell.y1+distance,cell.x2,cell.y2+ 2*distance)
            #find left
            cell.boundary["LEFT"] = self.findCell(cellList,cell.x1-distance,cell.y1,cell.x1,cell.y2)
            #find right
            cell.boundary["BOTTOM"] = self.findCell(cellList,cell.x1,cell.y1-distance,cell.x1+distance,cell.y2)
            #find bottom
            cell.boundary["RIGHT"] = self.findCell(cellList,cell.x1+distance,cell.y1,cell.x2+distance,cell.y2)

        for i,cell in enumerate(cellList):
            if cell.boundary["TOP"] is not None:
                cell.boundary["TOPLEFT"]=cell.boundary["TOP"].boundary["LEFT"]
            if cell.boundary["TOP"] is not None:
                    cell.boundary["TOPRIGHT"]=cell.boundary["TOP"].boundary["RIGHT"]
            if cell.boundary["BOTTOM"] is not None:
                        cell.boundary["BOTTOMRIGHT"]=cell.boundary["BOTTOM"].boundary["RIGHT"]
            if cell.boundary["BOTTOM"] is not None:
                        cell.boundary["BOTTOMLEFT"]=cell.boundary["BOTTOM"].boundary["LEFT"]
        return cellList

    def print_cellList(self,cellList):
        for cell in cellList:
            print("Cell : "+ str(cell.id))
            print("Boundaries are :")
            for x in cell.boundary:
                if cell.boundary[x] != None:
                    print("\t"+x+": "+ str(cell.boundary[x].id))
                else:
                    print("\t"+x+": None")

    def init_allocation(self,cellList,particleList):
        # print("Reallocating particles")
        for particle in particleList:
            particle.interacted = list()
            particle.spring_interacted = list()
            for i,cell in enumerate(cellList):
                cell.already_interacted = False
                # sys.stdout.write("\n {} : ({},{}) to ({},{})".format(cell.id,cell.x1,cell.y1,cell.x2,cell.y2))
                # input()
                if particle.x >= cell.x1 and particle.x <= cell.x2:
                    if particle.y >= cell.y1 and particle.y <= cell.y2:
                        # print("Alloted particle "+str(particle.id)+" to "+str(cell.id))
                        if particle.cell is not None:
                            original_cell = particle.cell
                            original_cell.remove_particle(particle)
                        cell.add_particle(particle)
                        particle.cell = cell
                        break
