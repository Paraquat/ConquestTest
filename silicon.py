import numpy as np
from static import StaticTest
from test import BlackBoxTest
from ase.build import bulk

def run_silicon(number, read=True):

  name = "silicon"
  grid_cutoff = 80.0
  xc = "LDA"
  kpts = [4,4,4]

  silicon = bulk('Si', 'diamond', a=5.563158, cubic=True)

  conquest_flags = {"DM.SolutionMethod": 'ordern',
                    "DM.L_range"       : 8.0,
                    "minE.LTolerance" : 1.0E-6}

  tester = StaticTest(number, name, silicon, 'minimal', verbose=True)
  bbtest = BlackBoxTest(tester, read)
  bbtest.run_test(grid_cutoff, xc, kpts, flags=conquest_flags)