import unittest
import importlib
import os

import gurutracker.globals
import gurutracker.helpers.fileopener
import gurutracker.config.py_configparser


class TestFileOpenerHelper(unittest.TestCase):
    def setUp(self):
        # fname = gurutracker.config.py_configparser.Config("testing.ini")
        # fname.read_config()
        gurutracker.globals.settings.set("files", "datadir", "DATA")
        gurutracker.globals.settings.write()
        
        importlib.reload(gurutracker.globals)
        
    def test_file_name(self):
        x = gurutracker.helpers.fileopener.filepath("MATH/HI")
        self.assertTrue(x == "DATA\\MATH\\HI.pdf")
        

def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFileOpenerHelper))
    # suite.addTest(unittest.makeSuite(Class2))
    return suite

if __name__ == '__main__':
   unittest.TextTestRunner(verbosity=2).run(suite())