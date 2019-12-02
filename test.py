import os.path
import numpy as np

class BlackBoxTest:

  def __init__(self, test_object, read=True, ref=False):
    self.tester = test_object
    self.read = read
    self.ref = ref
    self.stem = self.tester.get_path()
    if read:
      self.path = self.stem + ".ref"
    else:
      if ref:
        self.path = self.stem + ".ref"
      else:
        self.path = self.stem + ".dat"


  def run_test(self, grid_cutoff, xc, kpts, basis, flags={}):
    if self.read:
      self.tester.calculate(grid_cutoff, xc, kpts, basis, **flags)
      self.tester.read_reference(self.path)
      self.tester.compare()
    else:
      if os.path.isfile(self.path):
        print(f'{self.path} exists, skipping calculation')
      else:
        self.tester.calculate(grid_cutoff, xc, kpts, basis, **flags)
        self.tester.write_reference(self.path)
