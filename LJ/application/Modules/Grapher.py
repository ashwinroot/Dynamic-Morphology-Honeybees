import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.lines as mlines
import time
import sys
import os
import pickle
import numpy as np

def newline(p1, p2):
    ax = plt.gca()
    xmin, xmax = ax.get_xbound()

    if(p2[0] == p1[0]):
        xmin = xmax = p1[0]
        ymin, ymax = ax.get_ybound()
    else:
        ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
        ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])


class Grapher:
    def __init__(self,distance,iscellList=True):
        self.timestr = time.strftime("%YY%mM%dD-%HH%MM%SS")
        self.save_path = "output/" + self.timestr
        self.graph_time = 0
        self.distance = distance
        self.iscellList = iscellList


    def multi_plot(self,n_iter,particleList,cellList=list(),showPatch=True):
        tic1 = time.time()
        if not os.path.exists(self.save_path):
            sys.stdout.write("\n Created the file {}".format(self.save_path))
            os.makedirs(self.save_path)

        x ,y,a ,label= [] , [] , [],[]

        _width = 2
        narrow = 1/_width
        h = np.linspace(-6, 6, 1000)
        t = narrow* (h**2)

        for count,p in enumerate(particleList):
            x.append(p.x)
            y.append(p.y)
            a.append(p.potential)
            label.append(p.id)

        # with open(self.save_path+'/indump.pkl','a+b') as f:
        #     pickle.dump(particleList,f)


        fig = plt.figure()
        plt.title("Plotting "+str(n_iter))
        ax = plt.gca()
        ax.plot(h,t)
        plt.scatter(x,y,c=a)
        for i,l in enumerate(label):
            plt.annotate(str(l),xy=(x[i],y[i]))
        cbar = plt.colorbar()
        cbar.set_label("Potential", labelpad=+1)

        for particle in particleList:
            for t in particle.spring_interacted:
                l = mlines.Line2D([particle.x,particleList[t].x], [particle.y,particleList[t].y])
                ax.add_line(l)

        #grids
        if showPatch and self.iscellList:
            for cell in cellList:
                ax.add_patch(
                patches.Rectangle(
                    (cell.x1, cell.y1),
                    self.distance,
                    self.distance,
                    fill=False      ))# remove background
                plt.text(cell.x1-0.02*self.distance,cell.y1+0.02*self.distance,cell.id)

        plt.xlim((-7,7))
        plt.ylim((-7,7))

        fig.savefig(self.save_path+"/"+str(n_iter)+'.jpg')
        plt.close()

        tic2 = time.time()
        self.graph_time += tic2 - tic1


        #TODO:
#         import imageio
# import glob
#
# writer = imageio.get_writer('video.mp4', fps=0.2)
# for fname in glob.glob('images/*.jpg'):
#      img = imread(fname)
#     writer.append_data(img)
# writer.close()
