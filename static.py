import sys, os
from env import set_env
sys.path.append("/Users/zamaan/Conquest/ase/conquest")

import numpy as np
from ase.calculators.conquest import Conquest

from pdb import set_trace

vector_fmt = '{0:<20.10f}{1:<20.10f}{2:<20.10f}\n'

class StaticTest:

  def __init__(self, number, name, atoms, basis_size=None, verbose=False):
    self.number = number
    self.name = name
    self.atoms = atoms
    self.verbose = verbose

    self.fname = name + ".ref"
    self.natoms = len(self.atoms.positions)

    # Default energy, force, stress thresholds
    self.dE = 1.0E-8
    self.dF = 1.0E-5
    self.dS = 1E-3

    # Values to compare
    self.energy = None
    self.forces = None
    self.stress = None
    self.energy_ref = None
    self.forces_ref = None
    self.stress_ref = None
    self.basis = {}
    for species in self.atoms.get_chemical_symbols():
      self.basis[species] = {"basis_size": basis_size,
                             "gen_basis": True,
                             "pseudopotential_type": "hamann"}

  def set_thresh(self, dE=None, dF=None, dS=None):
    if dE:
      self.dE = dE

    if dF:
      self.dF = dF

    if dF:
      self.dS = dS

  def calculate(self, grid_cutoff, xc, kpts, **conquest_keywords):
    self.calc = Conquest(grid_cutoff=grid_cutoff,
                         xc=xc,
                         basis=self.basis,
                         kpts=kpts,
                         **conquest_keywords)
    self.atoms.set_calculator(self.calc)
    self.atoms.get_potential_energy()
    self.energy = self.atoms.calc.results["energy"]
    self.forces = self.atoms.calc.results["forces"]
    self.stress = self.atoms.calc.results["stress"][0:3]

  def compare(self):
    passed = True
    energy_diff = np.abs(self.energy - self.energy_ref)
    forces_diff = np.abs(self.forces - self.forces_ref)
    stress_diff = np.abs(self.stress - self.stress_ref)

    if energy_diff > self.dE:
      if self.verbose:
        print(f'Test {self.number}, {self.name} failed: dE = {self.energy_diff}')
      passed = False

    for i in range(self.natoms):
      for j in range(3):
        if forces_diff[i,j] > self.dF:
          if self.verbose:
            print(f'Test {self.number}, {self.name} failed: atom {i+1} component {j+1} dF = {forces_diff[i,j]}')
          passed = False

    for j in range(3):
      if stress_diff[j] > self.dS:
        if self.verbose:
          print(f'Test {self.number}, {self.name} failed: component {j+1} dS = {stress_diff[i,j]}')

    if passed:
      print(f'Test {self.number}, {self.name}... PASSED')
    else:
      print(f'Test {self.number}, {self.name}... FAILED')



  def read_reference(self):
    with open(self.fname, 'r') as infile:
      self.energy_ref = float(infile.readline().strip())
      self.forces_ref = []
      for i in range(self.natoms):
        self.forces_ref.append([float(f) for f in infile.readline().strip().split()])
      self.stress_ref = [float(s) for s in infile.readline().strip().split()]
      self.energy_ref = np.array(self.energy_ref)
      self.forces_ref = np.array(self.forces_ref)
      self.stress_ref = np.array(self.stress_ref)

  def write_reference(self):
    with open(self.fname, 'w') as outfile:
      outfile.write(f'{self.energy:<20.10f}\n')
      for f in self.forces:
        outfile.write(vector_fmt.format(*f))
      outfile.write(vector_fmt.format(*self.stress))