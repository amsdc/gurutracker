import unittest
import importlib
import os

import gurutracker.globals
import gurutracker.database.objects
import gurutracker.database.mysql

class TestObjects(unittest.TestCase):
    def test_equalness_objects(self):
        sub1 = gurutracker.database.objects.Subject(id=1, uidentifier="DDD")
        sub2 = gurutracker.database.objects.Subject(id=2)
        sub3 = gurutracker.database.objects.Subject(id=3, uidentifier="NNN")
        sub4 = gurutracker.database.objects.Subject(uidentifier="DDD")
        
        self.assertFalse(sub1 == sub2)
        self.assertFalse(sub2 == sub3)
        self.assertFalse(sub1 == sub3)
        self.assertTrue(sub1 == sub4)
        self.assertTrue(sub4 == sub1)
        self.assertFalse(sub4 == sub3)
        
        try:
            self.assertFalse(sub1 == 3.14)
        except Exception as e:
            self.assertTrue(isinstance(e, TypeError))

class TestMySQLController(unittest.TestCase):
    def setUp(self):
        # fname = gurutracker.config.py_configparser.Config("testing.ini")
        # fname.read_config()
        gurutracker.globals.settings.set("database", "type", "mysql")
        gurutracker.globals.settings.set("database", "host", "localhost")
        gurutracker.globals.settings.set("database", "user", "root")
        gurutracker.globals.settings.set("database", "password", os.environ.get("GURUTRACKER_TESTING_MYSQLPW", ""))
        gurutracker.globals.settings.set("database", "database", "gurutrackertest")
        gurutracker.globals.settings.write()
        
        importlib.reload(gurutracker.globals)
    
    def test_add_subject(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        self.assertTrue(sub.id is not None)
        sub2 = gurutracker.globals.controller.list_all_subjects()[0]
        self.assertTrue(sub == sub2)
    
    def tearDown(self):
        cur = gurutracker.globals.controller.con.cursor()
        cur.execute("DELETE FROM `subject`;")
        cur.execute("DELETE FROM `tutor`;")
        cur.execute("DELETE FROM `assignment`;")
        cur.execute("DELETE FROM `tag`;")
        gurutracker.globals.controller.con.commit()
        cur.close()
    
class TestSqlite3Controller(unittest.TestCase):
    pass
    
def suite():
    """ This defines all the tests of a module"""
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(TestObjects))
    suite.addTest(unittest.makeSuite(TestMySQLController))
    suite.addTest(unittest.makeSuite(TestSqlite3Controller))
    return suite

if __name__ == '__main__':
   unittest.TextTestRunner(verbosity=2).run(suite())