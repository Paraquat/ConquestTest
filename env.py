import os, sys

class ConquestEnv:

  def __init__(self, cq_exe, nprocs, pp_path, makeion_exe, ase_path):
    self.cq_exe = cq_exe
    self.nprocs = nprocs
    self.pp_path = pp_path
    self.makeion_exe = makeion_exe
    self.ase_path = ase_path
    self.mpi_command = 'mpirun'
    self.mpi_nproc_flag = '-np'
    self.set_ase_path(self.ase_path)
    self.set_cq_command(self.nprocs, self.cq_exe)
    self.set_makeion_exe(self.makeion_exe)
    self.set_pp_path(self.pp_path)

  def set_ase_path(self, ase_path):
    sys.path.append(ase_path)

  def set_cq_exe(self, cq_exe):
    self.cq_exe = cq_exe

  def set_mpi_command(self, mpi_command, mpi_nproc_flag):
    self.mpi_command = mpi_command
    self.mpi_nproc_flag = mpi_nproc_flag

  def set_cq_command(self, nprocs, cq_exe):
    self.cq_command = f'{self.mpi_command} {self.mpi_nproc_flag} {nprocs} {cq_exe}'
    os.environ["ASE_CONQUEST_COMMAND"] = self.cq_command

  def set_nprocs(self, nprocs):
    self.cq_command = f'{self.mpi_command} {self.mpi_nproc_flag} {nprocs} {self.cq_exe}'
    os.environ["ASE_CONQUEST_COMMAND"] = self.cq_command

  def set_makeion_exe(self, makeion_exe):
    self.makeion_exe = makeion_exe
    os.environ["CQ_GEN_BASIS_CMD"] = self.makeion_exe

  def set_pp_path(self, pp_path):
    self.pp_path = pp_path
    os.environ["CQ_PP_PATH"] = self.pp_path
