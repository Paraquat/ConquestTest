import numpy as np
from static import StaticTest
from test import BlackBoxTest
from ase import Atoms

def run_water_molecule(number, read=True):

  name = "H2O"
  grid_cutoff = 100.0
  xc = "PBE"
  kpts = [1,1,1]

  positions = [(3.9688293675, 3.9688293675, 3.9688293675),
               (3.9688293675, 4.7396710057, 3.3695305912),
               (3.9688293675, 3.1979854637, 3.3695334984)]
  water = Atoms(name, positions=positions)
  water.set_cell(8*np.identity(3))

  tester = StaticTest(number, name, water, 'medium', verbose=True)
  bbtest = BlackBoxTest(tester, read)
  bbtest.run_test(grid_cutoff, xc, kpts)
