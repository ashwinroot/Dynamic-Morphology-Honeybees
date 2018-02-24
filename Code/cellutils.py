from Cell import Cell
from Particle import Particle
import numpy as np

class CellUtils():
    def __init__(self):
        self.bound = {"x1": None,"y1": None,"x2": None,"y2":None}

        pass

    def findCell(self,cellList,startx,starty,endx,endy):
        for i,cell in enumerate(cellList):
            # print(i)
            if cell.x1 ==startx and cell.y1 ==starty:
                # print("Found cell")
                # input()
                return cell
        return None

    def init_cells(self,particleList,distance=1.5):
        print("\n Initialising cells")
        num_particles = particleList
        cellList = []
        b_x1,b_y1,b_x2,b_y2 = 0,0,0,0
        #getting the bounds of the system (#ask orit)
        counter = "A"
        for particle in particleList:
            if particle.x < b_x1:
                b_x1 = particle.x
            if particle.y < b_y1:
                b_y1 = particle.y
            if particle.x > b_x2:
                b_x2 = particle.x
            if particle.y > b_y2:
                b_y2 = particle.y

        length = np.sqrt((b_x1+b_x2)**2 + (b_y1-b_y2)**2)
        num_cell = int(length / distance)
        self.bound["x1"] = b_x1
        self.bound["x2"] = b_x2
        self.bound["y1"] = b_y1
        self.bound["y2"] = b_y2

        # initialising the x,y s of cells
        for i in range(num_cell):
            for j in range(num_cell):
                cellList.append(Cell(counter,b_x1+distance*i , b_y1+distance*j, b_x2+distance*i,b_y2+distance*j,distance))
                counter = chr(ord(counter)+1) #incrementing ascii

        #ADJACENT CELL FILLING
        for i, cell in enumerate(cellList):
            # print(i)
            #find top
            cell.boundary["RIGHT"] = self.findCell(cellList,cell.x1,cell.y1+distance,cell.x2,cell.y2+ 2*distance)
            #find left
            cell.boundary["TOP"] = self.findCell(cellList,cell.x1-distance,cell.y1,cell.x2- 2*distance,cell.y2)
            #find right
            cell.boundary["BOTTOM"] = self.findCell(cellList,cell.x1+2*distance,cell.y1,cell.x2+distance,cell.y2)
            #find bottom
            cell.boundary["LEFT"] = self.findCell(cellList,cell.x1,cell.y1-distance,cell.x2,cell.y2-distance)
        return cellList

        def print_cellList(self,cellList):
            for cell in cellList:
                print("Cell : "+ str(cell.id))
                print("Boundaries are :")
                for x in cell.boundary:
                    if cell.boundary[x] != None:
                        print("\t "+x+": "+ str(cell.boundary[x].id))
                    else:
                        print("\t"+x+": None");
