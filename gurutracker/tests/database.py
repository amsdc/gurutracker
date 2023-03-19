import unittest
import importlib
import os

import gurutracker.globals
import gurutracker.database.objects
import gurutracker.database.mysql


class TestObjects(unittest.TestCase):
    def test_assignment_list_typecast(self):
        ass = ["1", "Assn", "ASS", "summary", "1", "wdwd", "WDWD", "1", "effefe", "effef S", "QAAA"]
        assobj = gurutracker.database.objects.Assignment.from_list(ass)
        self.assertEqual(assobj.id, int(ass[0]))
        self.assertEqual(assobj.name, ass[1])
        self.assertEqual(assobj.uidentifier, ass[2])
        self.assertEqual(assobj.type, ass[3])
        self.assertEqual(assobj.tutor.id, int(ass[4]))
        self.assertEqual(assobj.tutor.name, ass[5])
        self.assertEqual(assobj.tutor.uidentifier, ass[6])
        self.assertEqual(assobj.tutor.subject.id, int(ass[7]))
        self.assertEqual(assobj.tutor.subject.name, ass[8])
        self.assertEqual(assobj.tutor.subject.desc, ass[9])
        self.assertEqual(assobj.tutor.subject.uidentifier, ass[10])

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
        # gurutracker.globals.settings.set("database", "host", "localhost")
        # gurutracker.globals.settings.set("database", "user", "root")
        # gurutracker.globals.settings.set("database", "password", os.environ.get("GURUTRACKER_TESTING_MYSQLPW"))
        # gurutracker.globals.settings.set("database", "database", "gurutrackertest")
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
    
    def test_add_subject_id(self):
        sub = gurutracker.database.objects.Subject(id=7,
                                                   name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        self.assertIsNotNone(sub.id)
        sub2 = gurutracker.globals.controller.list_all_subjects()[0]
        self.assertEqual(sub, sub2)
        self.assertEqual(sub2.id, 7)
        
    def test_get_subject_by_uid(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        self.assertTrue(sub.id is not None)
        sub2 = gurutracker.globals.controller.get_subject_by_uid("PHY")
        sub3 = gurutracker.globals.controller.get_subject_by_uid("PHYSICS")
        self.assertEqual(sub, sub2)
        self.assertTrue(sub2)
        self.assertIsNone(sub3)
        self.assertFalse(sub3)
        
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
    
    def test_add_tutor_with_id(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(id=8,
                                                   name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        self.assertIsNotNone(tutor.id)
        t = gurutracker.globals.controller.list_tutors()[0]
        self.assertEqual(t.id, 8)
    
    def test_get_tutor_by_uid(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        tuty = gurutracker.globals.controller.get_tutor_by_uid('FEYNMANN')
        tutn = gurutracker.globals.controller.get_tutor_by_uid('FEYMANN')
        self.assertEqual(tutor, tuty)
        self.assertTrue(tuty)
        self.assertIsNone(tutn)
        self.assertFalse(tutn)
        
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
        
    def test_add_assignment(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        self.assertIsNotNone(ass.id)
    
    def test_add_assignment_id(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(id=37,
                                                      name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        self.assertIsNotNone(ass.id)
        
        sd = gurutracker.globals.controller.list_all_assignments()[0]
        self.assertEqual(sd.id, 37)
    
    def test_add_unique_assignment(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        self.assertIsNotNone(ass.id)
        
        try:
            gurutracker.globals.controller.add_assignment(ass)
        except:
            self.assertTrue(1)
        else:
            self.assertTrue(0)
        
    def test_list_assignment(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        
        ass2 = gurutracker.database.objects.Assignment(name="Contour Integration",
                                                      uidentifier="TOOLS/MATH/CALCULUS/INT/CONTOUR",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass2)
        
        la = gurutracker.globals.controller.list_all_assignments()
        
        self.assertListEqual(la, [ass, ass2])
        self.assertEqual(la[0].name, "The Suction Tap")
        self.assertEqual(la[0].tutor, tutor)
        self.assertEqual(la[0].tutor.subject, sub)
        
    def test_edit_assignment(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        tutr = gurutracker.database.objects.Tutor(name="HC Verma",
                                                   uidentifier="HCV",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutr)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        
        ass.tutor = tutr
        gurutracker.globals.controller.edit_assignment(ass)
        la = gurutracker.globals.controller.list_all_assignments()[0]
        self.assertEqual(la.tutor, tutr)
        
    def test_get_assignment_uid(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        
        a2 = gurutracker.globals.controller.get_assignment_by_uid("FLUIDS/SUCTIONTAP")
        self.assertEqual(a2, ass)
    
    def test_del_assignment(self):
        sub = gurutracker.database.objects.Subject(name="Physics",
                                                   desc="Physics is the study of nature",
                                                   uidentifier="PHY")
        gurutracker.globals.controller.add_subject(sub)
        
        tutor = gurutracker.database.objects.Tutor(name="Richard Feymann",
                                                   uidentifier="FEYNMANN",
                                                   subject=sub)
        gurutracker.globals.controller.add_tutor(tutor)
        
        ass = gurutracker.database.objects.Assignment(name="The Suction Tap",
                                                      uidentifier="FLUIDS/SUCTIONTAP",
                                                      type="worksheet",
                                                      tutor=tutor)
        gurutracker.globals.controller.add_assignment(ass)
        
        self.assertEqual(len(gurutracker.globals.controller.list_all_assignments()), 1)
        
        gurutracker.globals.controller.del_assignment(ass)
        self.assertEqual(len(gurutracker.globals.controller.list_all_assignments()), 0)
    
    def test_add_tag(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        self.assertIsNotNone(tag.id)
        
        tag2 = gurutracker.database.objects.Tag(text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        self.assertIsNotNone(tag2.id)
    
    def test_add_tag_id(self):
        tag = gurutracker.database.objects.Tag(id=25,
                                               text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        self.assertIsNotNone(tag.id)
        
        tag2 = gurutracker.database.objects.Tag(id=29,
                                                text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        tt = gurutracker.globals.controller.list_tags()
        self.assertEqual(tt[0].id, 25)
        self.assertEqual(tt[1].id, 29)
    
    def test_list_tags(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        tag2 = gurutracker.database.objects.Tag(text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        tag3 = gurutracker.database.objects.Tag(text="Nonesence",
                                                fgcolor="FF0000",
                                                parent=tag2)
        gurutracker.globals.controller.add_tag(tag3)
        
        la = gurutracker.globals.controller.list_tags()
        
        self.assertListEqual(la, [tag, tag2, tag3])
        self.assertEqual(la[1].parent, tag)
        self.assertEqual(la[2].parent, tag2)
        self.assertEqual(la[2].parent.parent, tag)
        
    def test_list_tags_nopop(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        tag2 = gurutracker.database.objects.Tag(text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        tag3 = gurutracker.database.objects.Tag(text="Nonesence",
                                                fgcolor="FF0000",
                                                parent=tag2)
        gurutracker.globals.controller.add_tag(tag3)
        
        la = gurutracker.globals.controller.list_tags(populate_parents=False)
        
        self.assertListEqual(la, [tag, tag2, tag3])
        self.assertIsNone(la[1].parent)
        self.assertIsNone(la[2].parent)
    
    def test_edit_tags(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        tag2 = gurutracker.database.objects.Tag(text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        tag3 = gurutracker.database.objects.Tag(text="Nonesence",
                                                fgcolor="FF0000",
                                                parent=tag2)
        gurutracker.globals.controller.add_tag(tag3)
        
        tag3.parent = None
        gurutracker.globals.controller.edit_tag(tag3)
        
        tag2.text = "Elephants"
        gurutracker.globals.controller.edit_tag(tag2)
        
        la = gurutracker.globals.controller.list_tags()
        
        self.assertIsNone(la[2].parent)
        self.assertEqual(la[1].text, "Elephants")
        
    def test_del_tags(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        la = gurutracker.globals.controller.list_tags()
        self.assertEqual(len(la), 1)
        gurutracker.globals.controller.delete_tag(tag)
        la = gurutracker.globals.controller.list_tags()
        self.assertEqual(len(la), 0)
        
    def test_del_tags_nested(self):
        tag = gurutracker.database.objects.Tag(text="Physics")
        gurutracker.globals.controller.add_tag(tag)
        
        tag2 = gurutracker.database.objects.Tag(text="Fluids",
                                                fgcolor="FF0000",
                                                parent=tag)
        gurutracker.globals.controller.add_tag(tag2)
        
        tag3 = gurutracker.database.objects.Tag(text="Nonesence",
                                                fgcolor="FF0000",
                                                parent=tag2)
        gurutracker.globals.controller.add_tag(tag3)
        
        la = gurutracker.globals.controller.list_tags()
        self.assertEqual(len(la), 3)
        
        # delete 2 deletes 3 too
        gurutracker.globals.controller.delete_tag(tag2)
        la = gurutracker.globals.controller.list_tags()
        self.assertEqual(len(la), 1)
        self.assertEqual(la[0], tag)
    
    def tearDown(self):
        cur = gurutracker.globals.controller.con.cursor()
        cur.execute("DELETE FROM `assignment_tag`;")
        cur.execute("DELETE FROM `tag`;")
        cur.execute("DELETE FROM `assignment`;")
        cur.execute("DELETE FROM `tutor`;")
        cur.execute("DELETE FROM `subject`;")
        
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