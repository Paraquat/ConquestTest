import os
import os.path
import numpy as np
from pdb import set_trace

class TestIOHandler:
  """This class handles all file I/O for reference and test calculations

  Attributes
  ----------
  tester : StaticTest/EOSTest etc type object
    The CONQUEST test object
  ref : bool
    Toggle between reference calculation (True) and test calculation (False)
  ref_dir : str
    Directory for reference calculations and results
  test_dir : str
    Directory for test calculations and results
  ref_path : str
    Path to reference data file
  test_path : str
    Path to test data file
  """

  def __init__(self, test_object, ref=False):
    """Constructor for TestIOHandler

    Parameters
    ----------
    test_object : Test object
      of class StaticTest, EOSTest etc
    ref : bool (default False)
      Whether to do the reference calculation (True) or test calculation (False)
    """
    self.tester = test_object
    self.ref = ref
    self.ref_dir = "reference"
    self.test_dir = "test"
    name = self.tester.get_name
    self.ref_path = os.path.join(self.ref_dir, self.tester.get_name() + ".ref")
    self.test_path = os.path.join(self.test_dir, self.tester.get_name() + ".dat")
    if ref:
      self.mkdir(self.ref_dir)
    else:
      self.mkdir(self.test_dir)

  def mkdir(self, dir):
    """Make a directory if it doesn't already exist"""
    if not os.path.isdir(dir):
      os.mkdir(dir)

  def chdir(self, dir=None):
    """Change directory, save the base directory for switching back"""
    if dir:
      self.basedir = os.getcwd()
      os.chdir(dir)
    else:
      os.chdir(self.basedir)

  def run_test(self, grid_cutoff, xc, kpts, basis, flags={}):
    """Run the test

    If ref = True, do the reference calculation and store the results, otherwise
    read the reference results and compare them against the test calculation.

    Parameters
    ----------
    grid_cutoff : float
      Grid cutoff in Hartrees
    xc : str
      Exchange-correlation functional (LDA, PBE, etc.)
    kpts : list/dictionary
      K-points in list (Monkhorst-Pack mesh) or dictionary (see ASE documentation)
    basis : dictionary/str
      Either a dictionary of Conquest flags or a basis size
      (minimal, small, medium, large)
    flags : dictionary
      A dictionary of CONQUEST input flags to pass to the TestObject.calculate
    """
    if self.ref:
      if os.path.isfile(self.ref_path):
        print(f'{self.ref_path} exists, skipping calculation')
      else:
        self.chdir(self.ref_dir)
        self.tester.calculate(grid_cutoff, xc, kpts, basis, **flags)
        self.chdir()
        self.tester.write(self.ref_path)
    else:
      self.chdir(self.test_dir)
      self.tester.calculate(grid_cutoff, xc, kpts, basis, **flags)
      self.chdir()
      self.tester.read(self.ref_path)
      self.tester.compare()
      self.tester.write(self.test_path)
