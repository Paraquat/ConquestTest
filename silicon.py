import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_silicon(number, env, ref=False):
  """Silicon 8 atoms (diamond) SZ/ordern LDA """

  name = "silicon"
  description = "Silicon 8 atoms SZ order(N)"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [4,4,4]
  basis = {'Si' : {'file' : 'Si_SZ_v323_PBE.ion'}}
  env.set_nprocs(4)

  silicon = bulk('Si', 'diamond', a=5.563158, cubic=True)

  conquest_flags = {"DM.SolutionMethod": 'ordern',
                    "DM.L_range"       : 8.0,
                    "minE.LTolerance" : 1.0E-6}

  tester = StaticTest(number, name, description, silicon, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.set_ion_path(env.ion_path, basis)
  handler.run_test(grid_cutoff, xc, kpts, basis, flags=conquest_flags)
