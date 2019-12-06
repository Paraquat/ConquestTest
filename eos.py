import sys, os
from generic import GenericTest
import numpy as np
from ase.calculators.conquest import Conquest
from ase.io.trajectory import Trajectory
from ase.io import read
from ase.eos import EquationOfState

from pdb import set_trace

class EOSTest(GenericTest):
  """Subclass of GenericTest, used to compare two equation of state CONQUEST
  calculations

  Attributes
  ----------
  E0 : float
    Energy minimum from equation of state interpolation
  V0 : np.array (3 x natoms)
    Volume minimum from equation of state interpolation
  B : np.array (3)
    Bulk modulus from equation of state
  E0_ref : float
    Reference energy minimum
  V0_ref : np.array (3 x natoms)
    Reference equilibrium volume
  B_ref : np.array (3)
    Reference bulk modulus
  dE : float
    Energy threshold for comparison
  dV : float
    Volume threshold
  dB : float
    Bulk modulus threshold
  """

  def __init__(self, number, name, description, atoms, verbose=False,
               eos='birchmurnaghan'):
    """Constructor for EOSTTest

    Has one additional parameter compared with superclass:
    eos : string (default birchmurnaghan)
      The form of the equation of state as specified in the ASE EquationOfState class
    """
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
    """Determine the cell scaling factor grid for equation of state

    Single point calculations will be done for cells scaled +/- 0.01*vfactor

    Parameters
    ----------
    vfactor : float
      Minimum/maximum percentage by which to scale the lattice vectors
    ngrids : int
      Number of grid points (number of single point calculations to do)
    """
    vmin = 1.0 - 0.01*vfactor
    vmax = 1.0 + 0.01*vfactor
    self.grid = np.linspace(vmin, vmax, ngrids)
    self.volumes = np.zeros(ngrids)
    self.energies = np.zeros(ngrids)

  def calculate(self, grid_cutoff, xc, kpts, basis, **conquest_keywords):
    """Do single point CONQUEST calculations at each grid point, compute EOS

    Takes same parameters as superclass, but performs self.ngrids calculations, storing
    volumes and energies in self.volumes and self.energies respectivly
    """
    cell = self.atoms.get_cell()
    for i, x in enumerate(self.grid):
      self.atoms.set_cell(cell*x, scale_atoms=True)
      super().calculate(grid_cutoff, xc, kpts, basis, **conquest_keywords)
      self.volumes[i] = self.atoms.get_volume()
      self.energies[i] = self.atoms.calc.results["energy"]
      self.traj.write(self.atoms)
    self.get_eos(eos_type=self.eos)

  def set_thresh(self, dE=None, dV=None, dB=None):
    """Set thresholds for comparison against referece calculations"""
    if dE:
      self.dE = dE
    if dF:
      self.dF = dF
    if dF:
      self.dS = dS

  def read_traj(self, trajfile):
    """Read trajectory file which contains all single point calculations"""
    configs = read(f'{trajfile}@0:{self.ngrids}')
    self.volumes = [a.get_volume() for a in configs]
    self.energies = [a.get_potential_energy() for a in configs]

  def get_eos(self, eos_type='birchmurnaghan'):
    """Fit the equation of state"""
    eos = EquationOfState(self.volumes, self.energies, eos=eos_type)
    self.V0, self.E0, self.B = eos.fit()

  def compare(self):
    """Compare the test data against the reference data"""
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
    """Read the reference data from file

    File has the format:
    line 1: minimum energy
    line 2: equilibrium voluem
    line 3: bulk modullus
    lines 3-self.ngrids+3: volume, energy for each grid point"""
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
    """Write test/reference data to file"""
    with open(path, 'w') as outfile:
      eos_fmt = '{0:>20.10f}{1:>20.10f}\n'
      outfile.write(f'{self.E0:<20.10f}\n')
      outfile.write(f'{self.V0:<20.10f}\n')
      outfile.write(f'{self.B:<20.10f}\n')
      for i in range(self.ngrids):
        outfile.write(eos_fmt.format(self.volumes[i], self.energies[i]))
    print(f'Test {self.number}, {self.name}... data written to {path}')
