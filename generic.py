import sys, os
import os.path
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

  def calculate(self, grid_cutoff, xc, kpts, **conquest_keywords):
    self.calc = Conquest(grid_cutoff=grid_cutoff,
                         xc=xc,
                         basis=self.basis,
                         kpts=kpts,
                         **conquest_keywords)
    self.atoms.set_calculator(self.calc)
    self.atoms.get_potential_energy()

  def set_thresh(self, dE=None, dF=None, dS=None):
    if dE:
      self.dE = dE

    if dF:
      self.dF = dF

    if dF:
      self.dS = dS

  def print_fail(self, quantity, scalar, component=None, atom=None):
      if self.verbose:
        if component is None and atom is None:
          print(f'Test {self.number}, {self.name} failed: {quantity} = {scalar}')
        elif component is None:
          print(f'Test {self.number}, {self.name} failed: component {component+1} {quantity} = {scalar}')
        else:
          print(f'Test {self.number}, {self.name} failed: atom {atom+1} component {component+1} {quantity} = {scalar}')

  def print_result(self, passed):
    if passed:
      print(f'Test {self.number}, {self.name}... PASSED')
    else:
      print(f'Test {self.number}, {self.name}... FAILED')
