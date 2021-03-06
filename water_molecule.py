import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase import Atoms

def run_water_molecule(number, env, ref=False):
  """Water molecule 3 atoms DZP/diagonalisation PBE"""

  name = "H2O"
  description = "Water molecule DZP diagonalisation"
  grid_cutoff = 100.0
  xc = "PBE"
  kpts = [1,1,1]
  basis = {'H' : {'file' : 'H_DZP_v323_PBE.ion'},
           'O' : {'file' : 'O_DZP_v323_PBE.ion'}}
  env.set_nprocs(1)

  positions = [(3.9688293675, 3.9688293675, 3.9688293675),
               (3.9688293675, 4.7396710057, 3.3695305912),
               (3.9688293675, 3.1979854637, 3.3695334984)]
  water = Atoms(name, positions=positions)
  water.set_cell(8*np.identity(3))

  tester = StaticTest(number, name, description, water, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.set_ion_path(env.ion_path, basis)
  handler.run_test(grid_cutoff, xc, kpts, basis)
