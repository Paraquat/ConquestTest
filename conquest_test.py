#!/usr/local/bin/python3

"""CONQUEST functionality tests

This scripts performs CONQUEST functionality tests. A set of reference data can
be generated using the --reference flag, and compared against a calculation
by omitting the --reference flag.

usage: conquest_test.py [-h] [--reference] [--cqexe CQ_EXE]
                        [--basisgen MAKEION_EXE] [--pseudopath PP_PATH]
                        [--asepath ASE_PATH]

Run CONQUEST functionality tests

optional arguments:
  -h, --help            show this help message and exit
  --reference           Generate reference dataset (default: False)
  --cqexe CQ_EXE        Conquest executable (default: None)
  --basisgen MAKEION_EXE
                        Conquest basis generation tool executable (default:
                        MakeIonFiles)
  --pseudopath PP_PATH  Path to pseudopotential library (default: None)
  --asepath ASE_PATH    Path to ASE library (default: None)
"""

import argparse
from env import ConquestEnv

parser = argparse.ArgumentParser(description="Run CONQUEST functionality tests",
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--reference', action='store_true', dest='ref',
                    default=False, help='Generate reference dataset')
parser.add_argument('--cqexe', action='store', dest='cq_exe',
                    help='Conquest executable', default=None)
parser.add_argument('--basisgen', action='store', dest='makeion_exe',
                    help='Conquest basis generation tool executable', default='MakeIonFiles')
parser.add_argument('--pseudopath', action='store', dest='pp_path',
                    help='Path to pseudopotential library', default=None)
parser.add_argument('--asepath', action='store', dest='ase_path',
                    help='Path to ASE library', default=None)
cliopts = parser.parse_args()

env = ConquestEnv(cliopts.cq_exe, 1, cliopts.pp_path, cliopts.makeion_exe,
                  cliopts.ase_path)

from water_molecule import run_water_molecule
from diamond import run_diamond
from silicon import run_silicon
from diamond_mssf import run_diamond_mssf
from pto import run_pto
from ice import run_ice
from mgo import run_mgo
from silicon_eos import run_silicon_eos

if cliopts.ref:
  print('Generating reference data')
else:
  print('Running tests')

# Run the tests
run_water_molecule(1, env, ref=cliopts.ref)
run_diamond(2, env, ref=cliopts.ref)
run_silicon(3, env, ref=cliopts.ref)
run_diamond_mssf(4, env, ref=cliopts.ref)
run_pto(5, env, ref=cliopts.ref)
run_ice(6, env, ref=cliopts.ref)
run_mgo(7, env, ref=cliopts.ref)
run_silicon_eos(8, env, ref=cliopts.ref)
