import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_mgo(number, env, ref=False):
  """MgO 8 atoms (rocksalt) SZP/diagonalisation PBE """

  name = "MgO"
  description = "Magnesium Oxide 8 atoms SZP diagonalisation"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [4,4,4]
  basis = {'Mg' : {'file' : 'Mg_SZP_v323_PBE.ion'},
           'O'  : {'file' : 'O_SZP_v323_PBE.ion'}}
  env.set_nprocs(4)

  mgo = bulk('MgO', 'rocksalt', a=4.2798, cubic=True)

  tester = StaticTest(number, name, description, mgo, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.set_ion_path(env.ion_path, basis)
  handler.run_test(grid_cutoff, xc, kpts, basis)
