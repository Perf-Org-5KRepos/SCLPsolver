from scipy.io import mmwrite
from scipy.sparse import csr_matrix
import numpy as np


def write_CPLEX_dat(file_name, T, G, H, alpha, a, b, gamma, c):
    f1 = file_name + 'g.mtx'
    mmwrite(f1, csr_matrix(G))
    f2 = file_name + 'h.mtx'
    mmwrite(f2, csr_matrix(H))
    fout = open(file_name, 'w')
    fout.write('T = {:f};\r\n'.format(T))
    fout.write('VarDimension = {:d};\r\n'.format(G.shape[1]))
    fout.write('ConstrDimensionH = {:d};\r\n'.format(H.shape[0]))
    fout.write('ConstrDimensionG = {:d};\r\n'.format(G.shape[0]))
    fout.write('G = {\r\n')
    with open(f1,'r') as fp:
        line = fp.readline()
        while line:
            fout.write('<'+ line +'>\r\n')
        fp.close()
    fout.write( '};\r\n\r\n')
    fout.write('H = {\r\n')
    with open(f2, 'r') as fp:
        line = fp.readline()
        while line:
            fout.write('<' + line + '>\r\n')
        fp.close()
    fout.write('};\r\n\r\n')
    fout.write('alpha = {\r\n')
    for i in np.nonzero(alpha):
        fout.write('<{:d} {:d} {:.16f}>\r\n'.format(i,1,alpha[i]))
    fout.write('};\r\n\r\n')
    fout.write('a = {\r\n')
    for i in np.nonzero(a):
        fout.write('<{:d} {:d} {:.16f}>\r\n'.format(i, 1, a[i]))
    fout.write('};\r\n\r\n')
    fout.write('b = {\r\n')
    for i in np.nonzero(b):
        fout.write('<{:d} {:d} {:.16f}>\r\n'.format(i, 1, b[i]))
    fout.write('};\r\n\r\n')
    fout.write('c = {\r\n')
    for i in np.nonzero(c):
        fout.write('<{:d} {:d} {:.16f}>\r\n'.format(i, 1, c[i]))
    fout.write('};\r\n\r\n')
    fout.write('gamma = {\r\n')
    for i in np.nonzero(gamma):
        fout.write('<{:d} {:d} {:.16f}>\r\n'.format(i, 1, gamma[i]))
    fout.write('};\r\n\r\n')
    fout.close()