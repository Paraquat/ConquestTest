import os, sys

class EnvError(Exception):
  """Exceptions related to test environment

  Attributes
  ----------
  message : explanation of the error
  """

  def __init__(self, message):
    self.message = message

class ConquestEnv:

  def __init__(self, cq_exe, nprocs, ase_path=None, pp_path=None,
               makeion_exe=None, ion_path=None):
    if (not pp_path) and (not ion_path):
      raise EnvError("Either the pseudopotential path or the .ion path must \
        be specified.")
    self.cq_exe = cq_exe
    self.nprocs = nprocs
    self.mpi_command = 'mpirun'
    self.mpi_nproc_flag = '-np'
    self.set_cq_command(self.nprocs, self.cq_exe)
    self.ion_path = ion_path
    if ase_path:
      self.set_ase_path(ase_path)
    if makeion_exe:
      self.set_makeion_exe(makeion_exe)
    if pp_path:
      self.set_pp_path(pp_path)

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
