import unittest
import sys
sys.path.append("../../")
import pyABL.LES.wrfles as wrfles

class fileListTest(unittest.TestCase):

    def test_pathWithSlash(self):
        wrf=wrfles.WrfLES("./sample_data/")
	self.assertTrue(len(wrf.filelist)>0)

    def test_pathWithoutSlash(self):
	wrf=wrfles.WrfLES("./sample_data")
	self.assertTrue(len(wrf.filelist)>0)

    def test_pathNoWrfout(self):
	with self.assertRaises(IOError):
	    wrf=wrfles.WrfLES(".")

if __name__=="__main__":
	unittest.main()
