import pickle
import Particle
import LJ


file_name = "output/20180128-180153/dump.pkl"

with open(file_name,'rb') as f:
    x = pickle.load(f)
