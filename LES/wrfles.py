import numpy as np
import netCDF4 as nc
import glob

_wrfoutString = "wrfout_d*"

class wrfles(object):

    def __init__(self,wrfoutDir):

	"""Generate new wrfles object and populate it with paths to wrfout files
           to be used"""

        # wrfoutDir is expected to be full path from root directory to directory 
        # containing wrfout files
	self._wrfoutDir = wrfoutDir

	# user check: cover if user specifies directory with ending slash or not
	if self._wrfoutDir[-1] == '/':
	    self._filelist = sorted(glob.glob(self._wrfoutDir+_wrfoutString))
	else:
	    self._filelist = sorted(glob.glob(self._wrfoutDir+"/"+_wrfoutString))

	# if no wrfout files located, raise IOError to alert user.
	if len(self._filelist) < 1:
	    raise IOError("No WRF output files located in specified directory.")

    def list(self):

        """Lists wrfout files included in wrfles object file list"""

	files = list(li.split("/")[-1] for li in self._filelist)

        print files
	return files



if __name__ == "__main__":

    wrfles1 = wrfles("/lustre/scratch/tsliwins/L09KM/DX012AR1")
    wrfles1.list()
    wrfles2 = wrfles("/lustre/scratch/tsliwins/L09KM/DX012AR1/")
    #wrfles3 = wrfles("/lustre/scratch/tsliwins/L09KM/")

