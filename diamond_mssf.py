import numpy as np
from static import StaticTest
from iohandler import TestIOHandler
from ase.build import bulk

def run_diamond_mssf(number, ref=False):

  name = "diamond_mssf"
  description = "Diamond 8 atoms DZP/SZ multisite"
  grid_cutoff = 80.0
  xc = "LDA"
  kpts = [4,4,4]

  diamond = bulk('C', 'diamond', a=3.6, cubic=True)

  conquest_flags = {"Basis.MultisiteSF"         : True,
                    "Multisite.LFD"             : True,
                    "Multisite.LFD.Min.ThreshE" : 1.0E-7,
                    "Multisite.LFD.Min.ThreshD" : 1.0E-7,
                    "Multisite.LFD.Min.MaxIteration" : 150}
  basis = {"C": {"basis_size"            : "medium",
                 "gen_basis"             : True,
                 "pseudopotential_type"  : "hamann",
                 "Atom.NumberOfSupports" : 4,
                 "Atom.MultisiteRange"   : 7.0,
                 "Atom.LFDRange"         : 7.0}}

  tester = StaticTest(number, name, description, diamond, verbose=True)
  handler = TestIOHandler(tester, ref)
  handler.run_test(grid_cutoff, xc, kpts, basis, flags=conquest_flags)
