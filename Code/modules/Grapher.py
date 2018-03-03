import matplotlib.pyplot as plt
import matplotlib.patches as patches
import time
import sys
import os
import pickle

class Grapher:
    def __init__(self,distance):
        self.timestr = time.strftime("%YY%mM%dD-%HH%MM%SS")
        self.save_path = "output/" + self.timestr
        self.graph_time = 0
        self.distance = distance


    def multi_plot(self,n_iter,particleList,cellList,showPatch=True):
        distance = 1.5
        tic1 = time.time()
        if not os.path.exists(self.save_path):
            sys.stdout.write("\n Created the file {}".format(self.save_path))
            os.makedirs(self.save_path)

        x ,y,a ,label= [] , [] , [],[]

        for count,p in enumerate(particleList):
            x.append(p.x)
            y.append(p.y)
            a.append(p.potential)
            label.append(p.id)

        with open(self.save_path+'/indump.pkl','a+b') as f:
            pickle.dump(particleList,f)


        fig = plt.figure()
        plt.title("Plotting "+str(n_iter))
        ax = plt.gca()
        plt.scatter(x,y,c=a)
        for i,l in enumerate(label):
            plt.annotate(str(l),xy=(x[i],y[i]))
        cbar = plt.colorbar()
        cbar.set_label("Potential", labelpad=+1)

        #grids
        if showPatch:
            for cell in cellList:
                ax.add_patch(
                patches.Rectangle(
                    (cell.x1, cell.y1),
                    self.distance,
                    self.distance,
                    fill=False      # remove background
                )
                )

        # plt.xlim((b_x1-0.5,b_x2+0.5))
        # plt.ylim((b_y1-0.5,b_y2+0.5))

        fig.savefig(self.save_path+"/"+str(n_iter)+'.jpg')
        plt.close()

        tic2 = time.time()
        self.graph_time += tic2 - tic1
