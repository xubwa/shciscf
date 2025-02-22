#!/usr/bin/env python
# Copyright 2014-2020 The PySCF Developers. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Authors:  Sandeep Sharma <sanshar@gmail.com>
#           James Smith <james.smith9113@gmail.com>
#
"""
All output is deleted after the run to keep the directory neat. Comment out the
cleanup section to view output.
"""
import os, time

from pyscf import gto, scf, mcscf, dmrgscf
from pyscf.shciscf import shci

t0 = time.time()

#
# Mean Field
#

mol = gto.Mole()
mol.build(verbose=4, atom="C 0 0 0; C 0 0 1.8", basis="ccpvdz")
mf = scf.RHF(mol).run()

#
# Multireference
#
ncas = 8
nelecas = 8
mc = shci.SHCISCF(mf, ncas, nelecas)
mc.fcisolver.sweep_iter = [0, 3]
mc.fcisolver.sweep_epsilon = [1.0e-3, 1.0e-4]
print('hard coded sweep_iter:{:} and sweep_epsilon:{:}'.format(mc.fcisolver.sweep_iter, mc.fcisolver.sweep_epsilon))
mc.fcisolver.epsilon1 = 1e-4 # setting epsilon1 can automatically generate a sweep_iter and sweep_epsilon
print('automatically generated sweep_iter {:}'.format(mc.fcisolver.sweep_iter))
print('automatically generated sweep_epsilon {:}'.format(mc.fcisolver.sweep_epsilon))
mc.fcisolver.runtime_dir = "custom_runtime" # no need to manualy create this directory with the new interface.
mc.kernel()

print("Total Time:    ", time.time() - t0)

# File cleanup
mc.fcisolver.cleanup_dice_files()
