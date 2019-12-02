import numpy as np
from static import StaticTest
from test import BlackBoxTest
from ase.build import bulk

def run_diamond(number, read=True, ref=False):

  name = "diamond"
  grid_cutoff = 80.0
  xc = "LDA"
  kpts = [4,4,4]
  basis = "small"

  diamond = bulk('C', 'diamond', a=3.6, cubic=True)

  tester = StaticTest(number, name, diamond, verbose=True)
  bbtest = BlackBoxTest(tester, read, ref)
  bbtest.run_test(grid_cutoff, xc, kpts, basis)
