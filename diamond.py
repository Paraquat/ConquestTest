import numpy as np
from os.path import join
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_diamond(number, env, ref=False):
  """Carbon 8 atoms (diamond) SZP/diagonalisation LDA """

  name = "diamond"
  description = "Diamond 8 atoms SZP diagonalisation"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [4,4,4]
  basis = {'C' : {'file' : 'C_SZP_v323_PBE.ion'}}
  env.set_nprocs(4)

  diamond = bulk('C', 'diamond', a=3.6, cubic=True)

  tester = StaticTest(number, name, description, diamond, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.set_ion_path(env.ion_path, basis)
  handler.run_test(grid_cutoff, xc, kpts, basis)
