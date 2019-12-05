import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_mgo(number, ref=False):

  name = "MgO"
  description = "Magnesium Oxide 8 atoms SZP diagonalisation"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [4,4,4]
  basis = "small"
  mgo = bulk('MgO', 'rocksalt', a=4.2798, cubic=True)

  tester = StaticTest(number, name, description, mgo, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.run_test(grid_cutoff, xc, kpts, basis)
