import unittest
import importlib
import os

import gurutracker.globals
import gurutracker.database.objects
import gurutracker.database.mysql

class TestObjects(unittest.TestCase):
    def test_equalness_subject(self):
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
            
    def test_equalness_tutor(self):
        sub1 = gurutracker.database.objects.Tutor(id=1, uidentifier="DDD")
        sub2 = gurutracker.database.objects.Tutor(id=2)
        sub3 = gurutracker.database.objects.Tutor(id=3, uidentifier="NNN")
        sub4 = gurutracker.database.objects.Tutor(uidentifier="DDD")
        
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
            
    def test_equalness_assignment(self):
        sub1 = gurutracker.database.objects.Assignment(id=1, uidentifier="DDD")
        sub2 = gurutracker.database.objects.Assignment(id=2)
        sub3 = gurutracker.database.objects.Assignment(id=3, uidentifier="NNN")
        sub4 = gurutracker.database.objects.Assignment(uidentifier="DDD")
        
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
            
    def test_equalness_tag(self):
        sub1 = gurutracker.database.objects.Tag(id=1)
        sub2 = gurutracker.database.objects.Tag(id=2)
        sub3 = gurutracker.database.objects.Tag(id=3)
        sub4 = gurutracker.database.objects.Tag(id=1)
        
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
        gurutracker.globals.settings.set("database", "password", os.environ.get("GURUTRACKER_TESTING_MYSQLPW"))
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
        
    def test_edit_subject(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        sub.name = "Chemistry"
        gurutracker.globals.controller.edit_subject(sub)
        subr = gurutracker.globals.controller.list_all_subjects()[0]
        self.assertEqual(subr.name, "Chemistry")
        
    def test_del_subject(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        gurutracker.globals.controller.delete_subject(sub)
        subr = gurutracker.globals.controller.list_all_subjects()
        self.assertEqual(len(subr), 0)
    
    def test_add_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        self.assertIsNotNone(tutor.id)
        
    def test_add_unique_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        self.assertIsNotNone(tutor.id)
        
        try:
            gurutracker.globals.controller.add_tutor(tutor)
        except:
            self.assertTrue(1)
        else:
            self.assertTrue(0)
        
    def test_list_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        tutor3 = gurutracker.database.objects.Tutor(name="Ernico Fermi",
                                                   uidentifier="FERMI",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor3)
        
        l = gurutracker.globals.controller.list_tutors()
        self.assertListEqual(l, [tutor, tutor3])
    
    def test_edit_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        tutor.name = "good man"
        gurutracker.globals.controller.edit_tutor(tutor)
        
        t = gurutracker.globals.controller.list_tutors()[0]
        self.assertEqual(t.name, tutor.name)
    
    def test_edit_unique_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        tutor2 = gurutracker.database.objects.Tutor(name="Richard Feymann2",
                                                   uidentifier="FEYNMANN2",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        gurutracker.globals.controller.add_tutor(tutor2)
        
        tutor.uidentifier = "FEYNMANN2"
        
        try:
            gurutracker.globals.controller.edit_tutor(tutor)
        except:
            self.assertTrue(1)
        else:
            self.assertTrue(0)
    
    def test_del_tutor(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        gurutracker.globals.controller.delete_tutor(tutor)
        
        self.assertEqual(len(gurutracker.globals.controller.list_tutors()), 0)
    
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