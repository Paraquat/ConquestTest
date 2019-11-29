import sys, os
import os.path
sys.path.append("/Users/zamaan/Conquest/ase/conquest")

import numpy as np
from ase.calculators.conquest import Conquest

from pdb import set_trace


class GenericTest:

  def __init__(self, number, name, atoms, basis_size=None, verbose=False):
    self.number = number
    self.name = name
    self.atoms = atoms
    self.verbose = verbose

    self.natoms = len(self.atoms.positions)

    # Default energy, force, stress thresholds
    self.dE = 1.0E-8
    self.dF = 1.0E-5
    self.dS = 1E-3

    self.basis = {}
    for species in self.atoms.get_chemical_symbols():
      self.basis[species] = {"basis_size": basis_size,
                             "gen_basis": True,
                             "pseudopotential_type": "hamann"}

    # storing reference data
    refdir = "reference"
    if not os.path.isdir(refdir):
      os.mkdir(refdir)
    self.fname = os.path.join(refdir, name+".ref")

  def set_thresh(self, dE=None, dF=None, dS=None):
    if dE:
      self.dE = dE

    if dF:
      self.dF = dF

    if dF:
      self.dS = dS
