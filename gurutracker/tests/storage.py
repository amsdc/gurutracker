import io
import unittest
import importlib
import os
import tempfile

import gurutracker.globals
from gurutracker.storage.base import NoLinkedFileError, FileLinkageError
from gurutracker.storage.filesystem import FilesystemDirectory as FDSA
import gurutracker.config.py_configparser


class TestFilesystemDirectoryStorage(unittest.TestCase):
    def setUp(self):
        # fname = gurutracker.config.py_configparser.Config("testing.ini")
        # fname.read_config()
        self.dir = tempfile.TemporaryDirectory()
        
        self.fdsa = FDSA(self.dir.name)
    
    def tearDown(self):
        self.dir.cleanup()
        
    def test_add_file(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        bb = io.BytesIO()
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        
        self.assertTrue(os.path.isfile(os.path.join(self.dir.name, "file_0001")))
        
        bb.seek(0)
        f2 = open(os.path.join(self.dir.name, "file_0001"), "rb")
        self.assertEqual(f2.read(), bb.read())
        f2.close()
        f3 = open(os.path.join(self.dir.name, "extn_0001"), "r")
        self.assertEqual(f3.read(), "bin")
        f3.close()
        bb.close()
    
    def test_add_mtype(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        bb = io.BytesIO()
        bb.ext = "sha222"
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        
        f3 = open(os.path.join(self.dir.name, "extn_0001"), "r")
        self.assertEqual(f3.read(), "sha222")
        f3.close()
        # bb.close()
        
        # next
        ass.id = 3
        del bb.ext
        bb.name = "heel.pdm"
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        
        f3 = open(os.path.join(self.dir.name, "extn_0003"), "r")
        self.assertEqual(f3.read(), "pdm")
        f3.close()
        bb.close()
    
    def test_has_linked_file(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        
        self.assertFalse(self.fdsa.has_linked_file(ass))
        bb = io.BytesIO()
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        self.assertTrue(self.fdsa.has_linked_file(ass))
        bb.close()
    
    def test_get_file(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        
        try:
            self.fdsa.get_file(ass)
        except Exception as e:
            self.assertIsInstance(e, NoLinkedFileError)
        else:
            self.assertTrue(0, "No exc raised")
        bb = io.BytesIO()
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        bb.seek(0)
        f2 = self.fdsa.get_file(ass)
        self.assertEqual(f2.read(), bb.read())
        f2.close()
        bb.close()
    
    def test_get_file_type(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        
        try:
            self.fdsa.get_file(ass)
        except Exception as e:
            self.assertIsInstance(e, NoLinkedFileError)
        else:
            self.assertTrue(0, "No exc raised")
        bb = io.BytesIO()
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        # next
        ass.id = 3
        del bb.ext
        bb.name = "heel.pdm"
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        
        # chk
        ass.id = 1
        bb.seek(0)
        f2 = self.fdsa.get_file(ass)
        self.assertEqual(f2.ext, "bin")
        f2.close()
        
        ass.id = 3
        bb.seek(0)
        f2 = self.fdsa.get_file(ass)
        self.assertEqual(f2.ext, "pdm")
        f2.close()
        bb.close()
    
    def test_del_file(self):
        sub = gurutracker.database.objects.Subject(id=1,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        
        tutor = gurutracker.database.objects.Tutor(id=1,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        ass = gurutracker.database.objects.Assignment(id=1,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        bb = io.BytesIO()
        bb.write("This is a stupid binary file".encode("ascii"))
        bb.seek(0)
        self.fdsa.link_file(bb, ass)
        self.fdsa.unlink_file(ass)
        self.assertFalse(os.path.isfile(os.path.join(self.dir.name, "file_0001")))


def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestFilesystemDirectoryStorage))
    # suite.addTest(unittest.makeSuite(Class2))
    return suite

if __name__ == '__main__':
   unittest.TextTestRunner(verbosity=2).run(suite())