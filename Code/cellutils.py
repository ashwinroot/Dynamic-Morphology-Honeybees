from Cell import Cell
from Particle import Particle
import numpy as np

class CellUtils():
    def __init__(self):
        self.bound = {"x1": None,"y1": None,"x2": None,"y2":None}

        pass

    def init_cells(self,particleList,distance=1.5):
        num_particles = particleList
        cellList = []
        b_x1,b_y1,b_x2,b_y2 = 0,0,0,0
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
                
        length = np.sqrt((b_x1+b_x2)**2 + (b_y1-b_y2)**2)
        num_cell = int(length / distance)
        self.bound["x1"] = b_x1
        self.bound["x2"] = b_x2
        self.bound["y1"] = b_y1
        self.bound["y2"] = b_y2

        for i in range(num_cell):
            for j in range(num_cell):
                cellList.append(Cell(b_x1+distance*i , b_y1+distance*j, b_x2+distance*i,b_y2+distance*j,distance))

        # fig2,ax2= plt.subplots(1)
        # ax2 = plt.gca()
        # for cell in cellList:
        #     ax2.add_patch(
        #     patches.Rectangle(
        #         (cell.x1, cell.y1),
        #         distance,
        #         distance,
        #         fill=False      # remove background
        #     )
        #     )
        # plt.xlim((b_x1-0.5,b_x2+0.5))
        # plt.ylim((b_y1-0.5,b_y2+0.5))
        # fig2.savefig('rect2.png', dpi=90, bbox_inches='tight')
        return cellList

#     for cell in cellList:
#         rect = patches.Rectangle((float(cell.x1),float(cell.y1)),1.5,1.5,fill=False)
#         ax2.add_patch(rect)
#         plt.show()
