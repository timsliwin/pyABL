import unittest
from pyABL.LES import wrfles

class fileListTest(unittest.TestCase):

    def test_pathWithSlash(self):
        wrf=wrfles.wrfles("./sample_data/")
	self.assertTrue(len(wrf.list())>0)

    def test_pathWithoutSlash(self):
	wrf=wrfles.wrfles("./sample_data")
	self.assertTrue(len(wrf.list())>0)

    def test_pathNoWrfout(self):
	with self.assertRaises(IOError):
	    wrf=wrfles.wrfles(".")

if __name__=="__main__":
	unittest.main()
