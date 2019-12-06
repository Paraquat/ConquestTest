import sys, os
from generic import GenericTest
import numpy as np
from ase.calculators.conquest import Conquest
from ase.io.trajectory import Trajectory
from ase.io import read
from ase.eos import EquationOfState

from pdb import set_trace

class EOSTest(GenericTest):

  def __init__(self, number, name, description, atoms, verbose=False,
               eos='birchmurnaghan'):
    super().__init__(number, name, description, atoms, verbose)
    self.eos = eos
    self.trajfile = self.name+'.traj'
    self.traj = Trajectory(self.trajfile, 'w')

    # Values to compare
    self.E0 = None
    self.V0 = None
    self.B = None
    self.E0_ref = None
    self.V0_ref = None
    self.B_ref = None

    # Default grid: 2% variation in volume, 10 points
    self.delta = 2.0
    self.ngrids = 10
    self.set_grids(self.delta, self.ngrids)

    # Default comparison threshold
    self.dE = 1.0E-3
    self.dV = 1.0E-1
    self.dB = 1.0E-1

  def set_grids(self, vfactor, ngrids):
    vmin = 1.0 - 0.01*vfactor
    vmax = 1.0 + 0.01*vfactor
    self.grid = np.linspace(vmin, vmax, ngrids)
    self.volumes = np.zeros(ngrids)
    self.energies = np.zeros(ngrids)

  def calculate(self, grid_cutoff, xc, kpts, basis, **conquest_keywords):
    cell = self.atoms.get_cell()
    for i, x in enumerate(self.grid):
      self.atoms.set_cell(cell*x, scale_atoms=True)
      super().calculate(grid_cutoff, xc, kpts, basis, **conquest_keywords)
      self.volumes[i] = self.atoms.get_volume()
      self.energies[i] = self.atoms.calc.results["energy"]
      self.traj.write(self.atoms)
    self.get_eos(eos_type=self.eos)

  def set_thresh(self, dE=None, dV=None, dB=None):
    if dE:
      self.dE = dE
    if dF:
      self.dF = dF
    if dF:
      self.dS = dS

  def read_traj(self, trajfile):
    configs = read(f'{trajfile}@0:{self.ngrids}')
    self.volumes = [a.get_volume() for a in configs]
    self.energies = [a.get_potential_energy() for a in configs]

  def get_eos(self, eos_type='birchmurnaghan'):
    eos = EquationOfState(self.volumes, self.energies, eos=eos_type)
    self.V0, self.E0, self.B = eos.fit()

  def compare(self):
    passed = True
    E0_diff = np.abs(self.E0 - self.E0_ref)
    V0_diff = np.abs(self.V0 - self.V0_ref)
    B_diff = np.abs(self.B - self.B_ref)

    if E0_diff > self.dE:
      self.print_fail("deltaE", energy_diff)
      passed = False

    if V0_diff > self.dV:
      self.print_fail("deltaV", energy_diff)
      passed = False

    if B_diff > self.dB:
      self.print_fail("deltaB", energy_diff)
      passed = False

    self.print_result(passed)

  def read(self, path):
    with open(path, 'r') as infile:
      self.E0_ref = float(infile.readline().strip())
      self.V0_ref = float(infile.readline().strip())
      self.B_ref = float(infile.readline().strip())
      self.energies_ref = np.zeros(self.ngrids)
      self.volumes_ref = np.zeros(self.ngrids)
      for i in range(self.ngrids):
        self.volumes[i], self.energies[i] = \
          [float(s) for s in infile.readline().strip().split()]

  def write(self, path):
    with open(path, 'w') as outfile:
      eos_fmt = '{0:>20.10f}{1:>20.10f}\n'
      outfile.write(f'{self.E0:<20.10f}\n')
      outfile.write(f'{self.V0:<20.10f}\n')
      outfile.write(f'{self.B:<20.10f}\n')
      for i in range(self.ngrids):
        outfile.write(eos_fmt.format(self.volumes[i], self.energies[i]))
    print(f'Test {self.number}, {self.name}... data written to {path}')
