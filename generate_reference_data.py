#!/usr/local/bin/python3

from env import set_env

cq_exe = "Conquest_master" # Conquest executable
nprocs = 1                 # Number of MPI process for CONQUEST
pp_path = "/Users/zamaan/Conquest/PPDB/" # Path to pseudo database
makeion_exe = "MakeIonFiles"             # MakeIonFiles executable
ase_path = "/Users/zamaan/Conquest/ase/conquest" # path to ASE (CONQUEST) root
set_env(cq_exe, nprocs, pp_path, makeion_exe, ase_path)

from water_molecule import run_water_molecule
from diamond import run_diamond
from silicon import run_silicon

run_water_molecule(1, read=False)
nprocs = 4
set_env(cq_exe, nprocs, pp_path, makeion_exe, ase_path)
run_diamond(2, read=False)
run_silicon(3, read=False)
