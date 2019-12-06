import sys, os
from generic import GenericTest
import numpy as np
from ase.calculators.conquest import Conquest

from pdb import set_trace

class StaticTest(GenericTest):
  """Subclass of GenericTest, used to compare two static CONQUEST calculations

  Attributes
  ----------
  energy : float
    DFT total energy of the system
  forces : np.array (3 x natoms)
    Cartesian components of force on each atom
  stress : np.array (3)
    Cartesian components of stress on cell
  energy_ref : float
    Reference energy
  forces_ref : np.array (3 x natoms)
    Reference forces
  stress_ref : np.array (3)
    Reference stress
  dE : float
    Energy threshold for comparison with reference calculation
  dF : float
    Force threshold
  dS : float
    Stress threshold
  """

  def __init__(self, number, name, description, atoms, verbose=False):
    super().__init__(number, name, description, atoms, verbose)
    # Values to compare
    self.energy = None
    self.forces = None
    self.stress = None
    self.energy_ref = None
    self.forces_ref = None
    self.stress_ref = None

    # Default energy, force, stress thresholds
    self.dE = 1.0E-8
    self.dF = 1.0E-5
    self.dS = 1.0E-3

  def calculate(self, grid_cutoff, xc, kpts, basis, **conquest_keywords):
    """Perform a single point CONQUEST calculation

    Identical to method overloaded from GenericTest, except results are now
    class attibutes
    """
    super().calculate(grid_cutoff, xc, kpts, basis, **conquest_keywords)
    self.energy = self.atoms.calc.results["energy"]
    self.forces = self.atoms.calc.results["forces"]
    self.stress = self.atoms.calc.results["stress"][0:3]

  def set_thresh(self, dE=None, dF=None, dS=None):
    """Set the comparison thresholds"""
    if dE:
      self.dE = dE
    if dF:
      self.dF = dF
    if dF:
      self.dS = dS

  def compare(self):
    """Compare the test calculation results against the reference calculation"""
    passed = True
    energy_diff = np.abs(self.energy - self.energy_ref)
    forces_diff = np.abs(self.forces - self.forces_ref)
    stress_diff = np.abs(self.stress - self.stress_ref)

    if energy_diff > self.dE:
      self.print_fail("deltaE", energy_diff)
      passed = False

    for i in range(self.natoms):
      for j in range(3):
        if forces_diff[i,j] > self.dF:
          self.print_fail("deltaF", energy_diff, component=j, atom=i)
          passed = False

    for j in range(3):
      if stress_diff[j] > self.dS:
        self.print_fail("deltaS", energy_diff, component=j)

    self.print_result(passed)

  def read(self, path):
    """Read the reference data from file

    The file has the following format:
    line 1             : energy
    lines 2 - natoms+1 : 3 force components
    line natoms+2      : 3 stress components
    """
    with open(path, 'r') as infile:
      self.energy_ref = float(infile.readline().strip())
      self.forces_ref = []
      for i in range(self.natoms):
        self.forces_ref.append([float(f) for f in infile.readline().strip().split()])
      self.stress_ref = [float(s) for s in infile.readline().strip().split()]
      self.energy_ref = np.array(self.energy_ref)
      self.forces_ref = np.array(self.forces_ref)
      self.stress_ref = np.array(self.stress_ref)

  def write(self, path):
    """Write reference/test data to file"""
    vector_fmt = '{0:>20.10f}{1:>20.10f}{2:>20.10f}\n'

    with open(path, 'w') as outfile:
      outfile.write(f'{self.energy:<20.10f}\n')
      for f in self.forces:
        outfile.write(vector_fmt.format(*f))
      outfile.write(vector_fmt.format(*self.stress))
    print(f'Test {self.number}, {self.name}... data written to {path}')
