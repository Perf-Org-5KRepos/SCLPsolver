

class eta_matrix():

    __slots__= ['_v','_p']

    def __init__(self, v, p):
        self._v = v
        self._p = p

    @property
    def v(self):
        return self._v

    @property
    def p(self):
        return self._p

    # standard ftran operation on vector
    def ftran(self, vec):
        if vec[self._p] == 0:
            return vec
        else:
            ap = vec[self._p] * self._v[self._p]
            vv = vec + vec[self._p] * self._v
            vv[self._p] = ap
            return vv

    # inverse ftran operation on vector
    def inv_ftran(self, vec):
        if vec[self._p] == 0:
            return vec
        else:
            ap = vec[self._p] / self._v[self._p]
            vp = vec - self._v * ap
            vp[self._p] = ap
            return vp

    # standard ftran changing vector itself
    def fftran(self, vec):
        if vec[self._p] == 0:
            return vec
        else:
            ap = vec[self._p] * self._v[self._p]
            vec += vec[self._p] * self._v
            vec[self._p] = ap
            return vec

    # inverse ftran changing vector itself
    def inv_fftran(self, vec):
        if vec[self._p] == 0:
            return vec
        else:
            ap = vec[self._p] / self._v[self._p]
            vec -= self._v * ap
            vec[self._p] = ap
            return vec

    # produce eta matrix representation from vector
    @staticmethod
    def get_from_vector(vec, p):
        ap = -vec[p]
        vp = vec/ap
        vp[p] = -1/ap
        return eta_matrix(vp, p)

    # produce eta matrix representation using vectors before and after ftran
    @staticmethod
    def get_from_ftran(v2, v1, p):
        if v1[p] == 0:
            return None
        else:
            vp = (v2 - v1) / v1[p]
            vp[p] = v2[p]/v1[p]
            return eta_matrix(vp, p)

    # perform in place ftran without creation of eta matrix
    @staticmethod
    def get_fftran(vec, eta, p):
        if vec[p] == 0:
            return vec
        ap = vec[p]/eta[p]
        vec -= eta * ap
        vec[p] = ap
        return vec


import timeit
import numpy as np

# we assume primal_names_vector is already sorted in an ascending manner
# method should extract the variable in pivot_index location and enter a new variable name in the correct place in the vector (so the vector is still sorted)
def pivot_vector(primal_names_vector, primal_values_vector, eta_vector, pivot_index, entering_var_name):
    t = timeit.Timer('char in text', setup='text = "sample string"; char = "g"')

    new_primal_names_vector = []
    new_primal_values_vector = []

    for primal_name_vector_index, primal_name_vector_value in enumerate(primal_names_vector):

        if primal_name_vector_index != pivot_index:
            if primal_names_vector[primal_name_vector_index] > entering_var_name:
                # insert entering variable to new vector
                new_primal_names_vector.append(entering_var_name)
                new_primal_values_vector.append(primal_values_vector[pivot_index] * eta_vector[pivot_index])

                # insert next variable to keep the vector sorted
                new_primal_names_vector.append(primal_names_vector[primal_name_vector_index])
                new_primal_values_vector.append(primal_values_vector[primal_name_vector_index])
            else:
                # copy names/values as is
                new_primal_names_vector.append(primal_names_vector[primal_name_vector_index])
                new_primal_values_vector.append(primal_values_vector[primal_name_vector_index])

    print('time taken in milliseconds =', t.timeit()/1000)

    print('new_primal_names_vector =', new_primal_names_vector)
    print('new_primal_values_vector =', new_primal_values_vector)

    return [new_primal_names_vector, new_primal_values_vector]


print(pivot_vector([-15, -3, 1, 4], [1, 8, 5, -4], [3, 2, 1, 6], 1, 2))








