# cython: infer_types=True
# distutils: language = c++
#cython: language_level=3

from cython.parallel import prange
import numpy as np
cimport cython
from libcpp.vector cimport vector

@cython.boundscheck(False)
@cython.wraparound(False)
def get_prim_loc_mins(double[:,:] v):
    x_max = v.shape[0]
    y_max = v.shape[1]
    len_res = np.zeros(y_max-1, dtype=np.int32, order='C')
    cdef int[::1] len_res_view = len_res
    result = np.zeros((x_max, y_max-1), dtype=np.int32, order='F')
    cdef int[::1, :] result_view = result
    cdef int i, j, y
    for y in prange(y_max-1, nogil=True):
        j=0
        for i in range(x_max):
            if v[i,y] < 0 and v[i,y+1] > 0:
                result_view[j,y] = i
                j = j + 1
        len_res_view[y] = j
    return result, len_res

@cython.boundscheck(False)
@cython.wraparound(False)
def get_dual_loc_mins(double[:,:] v):
    x_max = v.shape[0]
    y_max = v.shape[1]
    len_res = np.zeros(y_max-1, dtype=np.int32, order='C')
    cdef int[::1] len_res_view = len_res
    result = np.zeros((x_max, y_max-1), dtype=np.int32, order='F')
    cdef int[::1, :] result_view = result
    cdef int i, j, y
    for y in prange(y_max-1, nogil=True):
        j=0
        for i in range(x_max):
            if v[i,y] > 0 and v[i,y+1] < 0:
                result_view[j,y] = i
                j = j + 1
        len_res_view[y] = j
    return result, len_res

@cython.boundscheck(False)
@cython.wraparound(False)
def get_loc_min(double[:] v1, double[:] v2):
    x_max = v1.shape[0]
    result = np.zeros(x_max, dtype=np.int32, order='C')
    cdef int[::1] result_view = result
    cdef int i, j
    j=0
    for i in range(x_max):
        if v1[i] < 0 and v2[i] > 0:
            result_view[j] = i
            j+=1
    return result[:j]

@cython.boundscheck(False)
@cython.wraparound(False)
def get_right_loc_min(double[:] v1):
    x_max = v1.shape[0]
    result = np.zeros(x_max, dtype=np.int32, order='C')
    cdef int[::1] result_view = result
    cdef int i, j
    j=0
    for i in range(x_max):
        if v1[i] < 0:
            result_view[j] = i
            j+=1
    return result[:j]

@cython.boundscheck(False)
@cython.wraparound(False)
def get_left_loc_min(double[:] v1):
    x_max = v1.shape[0]
    result = np.zeros(x_max, dtype=np.int32, order='C')
    cdef int[::1] result_view = result
    cdef int i, j
    j=0
    for i in range(x_max):
        if v1[i] > 0:
            result_view[j] = i
            j+=1
    return result[:j]

@cython.boundscheck(False)
@cython.wraparound(False)
def get_rz_bb(double[:, :] del_state, double[:, :] state, list loc_mins, list lens):
    cdef vector[int] vlens = lens
    cdef Py_ssize_t x_max = len(loc_mins)
    cdef int[:] lmin
    cdef int r_ind = -1, c_ind = -1, j_max, ind, i, j
    cdef double max_val = 0., val
    for i in range(x_max):
        j_max = vlens[i]
        lmin = loc_mins[i]
        for j in range(j_max):
            ind = lmin[j]
            val = del_state[ind, i]
            if val < 0.:
                val = -val / state[ind, i]
                if val > max_val:
                    r_ind = ind
                    c_ind = i
                    max_val = val
    return max_val, r_ind, c_ind


@cython.boundscheck(False)
@cython.wraparound(False)
def calc_state_prim(double[:, ::1] dv, int from_, int to_, double[::1] tau, double[::1] state0, bint checked = False):
    i_max = dv.shape[0]
    cdef int j_max = to_ - from_
    cdef Py_ssize_t i, j
    result = np.zeros((i_max, j_max+1), dtype= np.float64, order='C')
    cdef double[:,::1] result_view = result
    if state0 is not None:
        for i in range(i_max):
            result_view[i, 0] = state0[i]
    for i in prange(i_max, nogil=True):
        for j in range(j_max):
            if dv[i, j + from_] != 0. or checked:
                result_view[i, j+1] = dv[i, j + from_]  * tau[j] +  result_view[i, j]
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def calc_state_dual(double[:, ::1] dv, int from_, int to_, double[::1] tau, double[::1] state0, bint checked = False):
    i_max = dv.shape[0]
    cdef int j_max = to_ - from_
    cdef Py_ssize_t i, j
    result = np.zeros((i_max, j_max+1), dtype= np.float64, order='C')
    cdef double[:,::1] result_view = result
    if state0 is not None:
        for i in range(i_max):
            result_view[i, j_max] = state0[i]
    for i in prange(i_max, nogil=True):
        for j in range(j_max-1, -1, -1):
            if dv[i, j + from_] != 0. or checked:
                result_view[i, j] = dv[i, j + from_]  * tau[j] +  result_view[i, j+1]
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def calc_specific_state_prim(int n, int k, double[:, ::1] dv, int from_, int to_, double[::1] tau, double[::1] state0):
    cdef Py_ssize_t i
    cdef double result = 0
    if state0 is not None:
        result = state0[k]
    for i in range(n):
        if dv[k, i + from_] != 0.:
            result += dv[k, i + from_]  * tau[i]
    return result

@cython.boundscheck(False)
@cython.wraparound(False)
def calc_specific_state_dual(int n, int j, double[:, ::1] dv, int from_, int to_, double[::1] tau, double[::1] state0):
    cdef Py_ssize_t i
    cdef double result = 0
    cdef int j_max = to_ - from_
    if state0 is not None:
        result = state0[j]
    for i in range(j_max-1, n-1, -1):
        if dv[j, i + from_] != 0.:
            result += dv[j, i + from_]  * tau[i]
    return result
