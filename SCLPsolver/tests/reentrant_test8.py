import sys
sys.path.append('C:\DataD\Work\CERBERO\CLP\SCLPsolver')
from SCLP8 import SCLP
import os
import numpy as np


def relative_to_project(file_path):
    if os.path.isabs(file_path):
        return file_path
    else:
        proj = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), '..'))
        return os.path.join(proj, file_path)

seed = 1000
K = 600
I = 200
tmp_path =  relative_to_project('tests/data/reentrant/K'+str(K)+'/I' + str(I)+ '/seed' + str(seed)+ '/')
G = np.load(tmp_path + 'G.dat')
F = np.load(tmp_path + 'F.dat')
H = np.load(tmp_path + 'H.dat')
a = np.hstack(np.load(tmp_path + 'a.dat'))
b = np.hstack(np.load(tmp_path + 'b.dat'))
c = np.hstack(np.load(tmp_path + 'c.dat'))
d = np.load(tmp_path + 'd.dat')
if np.size(d) ==0:
    d = np.empty(shape=(0))
if np.size(F) ==0:
    F = np.empty(shape=(G.shape[0], 0))
print(F.shape)
#d = np.hstack(dd)
alpha = np.hstack(np.load(tmp_path + 'alpha.dat'))
gamma = np.hstack(np.load(tmp_path + 'gamma.dat'))
import time
start_time = time.time()
import cProfile, pstats, io
pr = cProfile.Profile()
pr.enable()
t, x, q, u, p, pivots, obj, err, NN, STEPCOUNT = SCLP(G, H, F, a, b, c, d, alpha, gamma, 500, {}, 1E-11, tmp_path)
print(obj, err)
print("--- %s seconds ---" % (time.time() - start_time))
pr.disable()
s = io.StringIO()
ps = pstats.Stats(pr, stream=s)
ps.print_stats()
print(s.getvalue())