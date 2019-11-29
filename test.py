import numpy as np

class BlackBoxTest:

  def __init__(self, test_object, read):
    self.tester = test_object
    self.read = read

  def run_test(self, grid_cutoff, xc, kpts, flags={}):
    self.tester.calculate(grid_cutoff, xc, kpts, **flags)
    if self.read:
      self.tester.read_reference()
      self.tester.compare()
    else:
      self.tester.write_reference()
