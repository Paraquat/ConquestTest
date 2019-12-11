import sys, os
import os.path
import numpy as np
from ase.calculators.conquest import Conquest

from pdb import set_trace


class GenericTest:
  """Base class for running conquest tests.

  Contains all information and code to run a single point CONQUEST calculation,
  but not do anything with it.

  Attributes
  ----------
  number : int
    Integer label for the test
  name : str
    String label for the test
  description : str
    Description of the test
  atoms : Atom object
    an ASE Atom object
  natoms : int
    Number of atoms
  """

  def __init__(self, number, name, description, atoms, verbose=False):
    """GenericTest constructor

    Parameters
    ----------
    number : int
      Integer label for the test
    name : str
      String label for the test
    description : str
      Description of the test
    atoms : Atom object
      an ASE Atom object
    verbose : bool, optional
      Print detailed comparison information
    """
    self.number = number
    self.name = name
    self.description = description
    self.atoms = atoms
    self.verbose = verbose
    self.natoms = len(self.atoms.positions)

  def calculate(self, grid_cutoff, xc, kpts, basis, **conquest_keywords):
    """Run a single point CONQUEST calculation

    Takes a minimal set of mandatory arguments for a DFT calculation:

    Parameters
    ----------
    grid_cutoff : float 
      The grid cutoff in Hartrees
    xc : str
      Exchange-correlation functional as a string (LDA, PBE, etc.)
    kpts : list/dict
      K-point list or Monkhorst-Pack mesh, as specified in the CONQUEST
      interface to ASE
    basis : dict/str
      Either a dictionary as specified in the CONQUEST/ASE interface, or
      a string specifying the basis size for MakeIonFiles (minimal, small,
      medium, large)
    conquest_flags : kwargs
      Typically a dictionary of CONQUEST key/value pairs
    """

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

  def get_name(self):
    """Return the name attribute"""
    return self.name

  def print_fail(self, quantity, scalar, component=None, atom=None):
    """If a test comparison is failed, print a message

    Parameters
    ----------
    quantity : str
      Name of the quantity being compared (delteE, deltaF etc.)
    scalar : int
      The value being compared
    component : int
      The cartesian direction (1, 2 or 3)
    atom : int
      The atomic index
    """
    if self.verbose:
      if component is None and atom is None:
        print(f'Test {self.number}, {self.name} failed: {quantity} = {scalar}')
      elif component is None:
        print(f'Test {self.number}, {self.name} failed: component {component+1} {quantity} = {scalar}')
      else:
        print(f'Test {self.number}, {self.name} failed: atom {atom+1} component {component+1} {quantity} = {scalar}')

  def print_result(self, passed):
    """Print the result of the test"""
    if passed:
      print(f'Test {self.number}, {self.description}... PASSED')
    else:
      print(f'Test {self.number}, {self.description}... FAILED')
