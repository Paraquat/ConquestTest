import os, sys

def set_env(cq_exe, nprocs, pp_path, makeion_exe, ase_path):
  sys.path.append(ase_path)
  os.environ["ASE_CONQUEST_COMMAND"] = f'mpirun -np {nprocs} {cq_exe}'
  os.environ["CQ_PP_PATH"] = pp_path
  os.environ["CQ_GEN_BASIS_CMD"] = makeion_exe
