import numpy as np
from eos import EOSTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_silicon_eos(number, env, ref=False):

  name = "silicon_eos"
  description = "Silicon 8 atoms SZ diagon equation of state"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [4,4,4]
  basis = "minimal"
  env.set_nprocs(4)

  silicon = bulk('Si', 'diamond', a=5.563158, cubic=True)

  tester = EOSTest(number, name, description, silicon, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.run_test(grid_cutoff, xc, kpts, basis)