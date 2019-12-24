import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase import Atoms

def run_pto(number, env, ref=False):
  """Lead titanate 6 atoms SZP/diagonalisation PBE """

  name = "PTO"
  description = "Lead titanate 5 atoms SZP diagonalisation"
  grid_cutoff = 80.0
  xc = "PBE"
  kpts = [9,9,9]
  basis = "small"
  basis = {'Pb' : {'file' : 'Pb_SZP_v323_PBE.ion'},
           'Ti' : {'file' : 'Ti_SZP_v323_PBE.ion'},
           'O'  : {'file' : 'O_SZP_v323_PBE.ion'}}
  conquest_flags = {"Diag.SmearingType": 0,
                    "Diag.kT"          : 0.0003674931}
  env.set_nprocs(2)

  a = 3.95
  positions = [(0.0, 0.0, 0.0),
               (0.5, 0.5, 0.5),
               (0.0, 0.5, 0.5),
               (0.5, 0.0, 0.5),
               (0.5, 0.5, 0.0)]
  pto = Atoms("PbTiO3", positions=positions)
  pto.set_cell(a*np.identity(3), scale_atoms=True)

  tester = StaticTest(number, name, description, pto, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.set_ion_path(env.ion_path, basis)
  handler.run_test(grid_cutoff, xc, kpts, basis, flags=conquest_flags)
