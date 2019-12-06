import sys, os
import os.path
import numpy as np
from ase.calculators.conquest import Conquest

from pdb import set_trace


class GenericTest:

  def __init__(self, number, name, description, atoms, verbose=False):
    self.number = number
    self.name = name
    self.description = description
    self.atoms = atoms
    self.verbose = verbose
    self.natoms = len(self.atoms.positions)

  def calculate(self, grid_cutoff, xc, kpts, basis, **conquest_keywords):

    # set up basis/.ion files
    if isinstance(basis, dict):
      self.basis = basis
    elif isinstance(basis, str):
      self.basis = {}
      for species in self.atoms.get_chemical_symbols():
        self.basis[species] = {"basis_size": basis,
                               "gen_basis": True,
                               "pseudopotential_type": "hamann"}

    self.calc = Conquest(label=self.name,
                         grid_cutoff=grid_cutoff,
                         xc=xc,
                         basis=self.basis,
                         kpts=kpts,
                         **conquest_keywords)
    self.atoms.set_calculator(self.calc)
    self.atoms.get_potential_energy()

  def set_exe(self, cq_command, nprocs, cq_exe):
    os.environ["ASE_CONQUEST_COMMAND"] = cq_command

  def get_name(self):
    return self.name

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
      print(f'Test {self.number}, {self.description}... PASSED')
    else:
      print(f'Test {self.number}, {self.description}... FAILED')
