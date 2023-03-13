import unittest
import os

import gurutracker.helpers.fileopener
import gurutracker.config.py_configparser


class TestFileOpenerHelper(unittest.TestCase):
    def test_file_name(self):
        fname = gurutracker.config.py_configparser.Config("testing.ini")
        fname.read_config()
        
        x = gurutracker.helpers.fileopener.filepath(fname, "MATH/HI")
        self.assertTrue(x == "DATA\\MATH\\HI.pdf")
        
        fname.config["files"]["datadir"] = "DATA/jjj"
        fname.write()
        x = gurutracker.helpers.fileopener.filepath(fname, "MATH/HI")
        self.assertTrue(x == "DATA\\jjj\\MATH\\HI.pdf")
        os.unlink("testing.ini")
        

def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFileOpenerHelper))
    # suite.addTest(unittest.makeSuite(Class2))
    return suite

if __name__ == '__main__':
   unittest.TextTestRunner(verbosity=2).run(suite())