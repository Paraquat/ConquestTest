import os
import os.path
import numpy as np
from pdb import set_trace

class TestIOHandler:

  def __init__(self, test_object, ref=False):
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
    if not os.path.isdir(dir):
      os.mkdir(dir)

  def chdir(self, dir=None):
    if dir:
      self.basedir = os.getcwd()
      os.chdir(dir)
    else:
      os.chdir(self.basedir)

  def run_test(self, grid_cutoff, xc, kpts, basis, flags={}):
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
