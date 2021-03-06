# Copyright 2020 IBM Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np


class solution_state():
    __slots__ = ['dx','dq', 'x','q','del_x','del_q','_tau','dtau','_max_tau_size','_tau_size']

    def __init__(self, max_tau_size, JJ, KK):
        self._max_tau_size = max_tau_size
        self._tau = np.zeros(self._max_tau_size, dtype=np.double, order='C')
        #TODO: further improvement can be provided if we reuse states between iterations
        self.x = np.zeros((KK, self._max_tau_size+1), dtype=np.float64, order='C')
        self.del_x = np.zeros((KK, self._max_tau_size+1), dtype=np.float64, order='C')
        self.q = np.zeros((JJ, self._max_tau_size+1), dtype=np.float64, order='C')
        self.del_q = np.zeros((JJ, self._max_tau_size+1), dtype=np.float64, order='C')
        self._tau_size = 0
        self.dtau = None

    def update_tau(self, col_info, initT = 0, backward = False):
        if self.dtau is None:
            self._tau_size = 1
            self._tau[0] = initT
        else:
            if backward:
                #TODO understand when we need this and complete
                self._tau[:self._tau_size] -= self.dtau * col_info.delta
            else:
                self._tau[:self._tau_size] += self.dtau * col_info.delta
                if col_info.Nnew != 0:
                    if col_info.Nnew + self._tau_size > self._max_tau_size:
                        self._enlarge((col_info.Nnew + self._tau_size)*2)
                    new_size = self._tau_size+col_info.Nnew
                    self._tau[col_info.N2 + col_info.Nnew:new_size] = self._tau[col_info.N2:self._tau_size]
                    self._tau_size = new_size
                if col_info.Nnew > 0:
                    self._tau[col_info.N2:col_info.N2 + col_info.Nnew] = 0.

    def _enlarge(self, size):
        self._max_tau_size = size
        tau = np.zeros(self._max_tau_size, dtype=np.double, order='C')
        tau[:self._tau_size] = self._tau[:self._tau_size]
        self._tau = tau
        self.reserve_memory_for_states()

    @property
    def tau(self):
        return self._tau[:self._tau_size]

    @tau.setter
    def tau(self, value):
        self._tau_size = value.shape[0]
        if self._tau_size > self._max_tau_size:
            self._max_tau_size = self._tau_size * 2
            self._tau = np.zeros(self._max_tau_size, dtype=np.double, order='C')
            self.reserve_memory_for_states()
        self._tau[:self._tau_size] = value

    def reserve_memory_for_states(self):
        self.x = np.zeros((self.x.shape[0], self._max_tau_size + 1), dtype=np.float64, order='C')
        self.del_x = np.zeros((self.del_x.shape[0], self._max_tau_size + 1), dtype=np.float64, order='C')
        self.q = np.zeros((self.q.shape[0], self._max_tau_size + 1), dtype=np.float64, order='C')
        self.del_q = np.zeros((self.del_q.shape[0], self._max_tau_size + 1), dtype=np.float64, order='C')