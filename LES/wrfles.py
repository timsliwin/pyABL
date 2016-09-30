import numpy as np
import netCDF4 as nc
import glob

class WrfLES(object):

    def __init__(self,wrfoutDir):

	self.wrfoutDir = wrfoutDir

	if self.wrfoutDir[-1] == '/':
	    self.filelist = glob.glob(self.wrfoutDir+"wrfout*")
	else:
	    self.filelist = glob.glob(self.wrfoutDir+"/wrfout*")
	    
	print self.filelist

	if len(self.filelist) < 1:
	    raise IOError("No WRF output files located in specified directory.")

if __name__ == "__main__":

    wrfles1 = WrfLES("/lustre/scratch/tsliwins/L09KM/DX012AR1")
    wrfles2 = WrfLES("/lustre/scratch/tsliwins/L09KM/DX012AR1/")
    wrfles3 = WrfLES("/lustre/scratch/tsliwins/L09KM/")
