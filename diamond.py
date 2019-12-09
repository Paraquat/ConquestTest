import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_diamond(number, env, ref=False):
  """Carbon 8 atoms (diamond) SZP/diagonalisation LDA """

  name = "diamond"
  description = "Diamond 8 atoms SZP diagonalisation"
  grid_cutoff = 80.0
  xc = "LDA"
  kpts = [4,4,4]
  basis = "small"
  env.set_nprocs(4)

  diamond = bulk('C', 'diamond', a=3.6, cubic=True)

  tester = StaticTest(number, name, description, diamond, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.run_test(grid_cutoff, xc, kpts, basis)
