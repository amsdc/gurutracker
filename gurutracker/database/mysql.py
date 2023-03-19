import pymysql

from gurutracker.database.base import Base
from gurutracker.database.objects import Subject, Tutor, Assignment, Tag

class Controller(Base):
    def __init__(self, connection):
        self.con = connection
    
    def list_all_subjects(self):
        """list_all_subjects 
        
        List all subjects.
        """
        cur = self.con.cursor()
        cur.execute("SELECT `id`, `name`, `desc`, `uidentifier` FROM `subject`;")
        res = []
        for item in cur.fetchall():
            res.append(Subject(id=item[0],
                               name=item[1],
                               desc=item[2],
                               uidentifier=item[3]))
        cur.close()
        return res
    
    def get_subject_by_uid(self, uid):
        cur = self.con.cursor()
        cur.execute("SELECT `id`, `name`, `desc`, `uidentifier` FROM `subject` WHERE `uidentifier`=%s LIMIT 1;", (uid, ))
        res = None
        item = cur.fetchone()
        if item:
            res = Subject(id=item[0],
                          name=item[1],
                          desc=item[2],
                          uidentifier=item[3])
        cur.close()
        return res
    
    def add_subject(self, subject):
        cur = self.con.cursor()
        if subject.id: # has id, so use it
            cur.execute("INSERT INTO `subject` (`id`, `name`, `desc`, `uidentifier`) VALUES (%s, %s, %s, %s);", (subject.id, subject.name, subject.desc, subject.uidentifier))
            self.con.commit()
        else: # put the id in obj
            cur.execute("INSERT INTO `subject` (`name`, `desc`, `uidentifier`) VALUES (%s, %s, %s);", (subject.name, subject.desc, subject.uidentifier))
            self.con.commit()
            cur.execute("SELECT `id` FROM `subject` WHERE `uidentifier`=%s LIMIT 1;", (subject.uidentifier,))
            subject.id = cur.fetchone()[0]
        cur.close()
    
    def edit_subject(self, subject):
        cur = self.con.cursor()
        cur.execute("UPDATE `subject` SET `name`=%s, `desc`=%s, `uidentifier`=%s WHERE `id`=%s", (subject.name, subject.desc, subject.uidentifier, subject.id))
        self.con.commit()
        cur.close()
    
    def delete_subject(self, subject):
        cur = self.con.cursor()
        cur.execute("DELETE FROM `subject` WHERE  `id`=%s", (subject.id,))
        self.con.commit()
        cur.close()
        
    def list_all_assignments(self):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` ORDER BY `assignment`.`id` ASC;")
        res = []
        for item in cur.fetchall():
            sub = Subject(id=item[7],
                          name=item[8],
                          desc=item[9],
                          uidentifier=item[10])
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=sub)
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            res.append(ass)
        cur.close()
        return res

    def list_all_assignments_customsql(self, custom_sql):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `subject` ON `tutor`.`subid` = `subject`.`id`" + custom_sql + ";")
        res = []
        for item in cur.fetchall():
            sub = Subject(id=item[7],
                          name=item[8],
                          desc=item[9],
                          uidentifier=item[10])
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=sub)
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            res.append(ass)
        cur.close()
        return res
        
    def get_assignment_by_id(self, id):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` WHERE `assignment`.`id`=%s LIMIT 1;", (id,))
        item = cur.fetchone()
        if item:
            sub = Subject(id=item[7],
                          name=item[8],
                          desc=item[9],
                          uidentifier=item[10])
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=sub)
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            cur.close()
            return ass
    
    def get_assignment_by_uid(self, uid):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` WHERE `assignment`.`uidentifier`=%s LIMIT 1;", (uid,))
        item = cur.fetchone()
        if item:
            sub = Subject(id=item[7],
                          name=item[8],
                          desc=item[9],
                          uidentifier=item[10])
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=sub)
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            cur.close()
            return ass
    
    def search_assignment_by_name_instr(self, name):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment`, `tutor` WHERE `assignment`.`tid` = `tutor`.`id` AND `assignment`.`name` LIKE %s ORDER BY `assignment`.`id` ASC;", ("%"+name+"%",))
        res = []
        for item in cur.fetchall():
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=item[7],
                         level=item[8])
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            res.append(ass)
        cur.close()
        return res

    def search_uid_by_name_instr(self, name):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment`, `tutor` WHERE `assignment`.`tid` = `tutor`.`id` AND `assignment`.`uidentifier` LIKE %s ORDER BY `assignment`.`id` ASC;", ("%"+name+"%",))
        res = []
        for item in cur.fetchall():
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=item[7],
                         level=item[8])
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            res.append(ass)
        cur.close()
        return res
    
    def search_assignment_by_tags(self, tags):
        raise NotImplementedError
        
    def add_assignment(self, assignment):
        cur = self.con.cursor()
        if assignment.id: # use id given
            cur.execute("INSERT INTO `assignment` (`id`, `name`, `uidentifier`, `type`, `tid`) VALUES (%s, %s, %s, %s, %s);", (assignment.id, assignment.name, assignment.uidentifier, assignment.type, assignment.tutor.id))
            self.con.commit()
        else:
            cur.execute("INSERT INTO `assignment` (`name`, `uidentifier`, `type`, `tid`) VALUES (%s, %s, %s, %s);", (assignment.name, assignment.uidentifier, assignment.type, assignment.tutor.id))
            self.con.commit()
            cur.execute("SELECT `id` FROM `assignment` WHERE `uidentifier`=%s LIMIT 1;", (assignment.uidentifier,))
            assignment.id = cur.fetchone()[0]
        cur.close()
    
    def edit_assignment(self, assignment):
        cur = self.con.cursor()
        cur.execute("UPDATE `assignment` SET `name` = %s, `uidentifier` = %s, `type` = %s, `tid` = %s WHERE `id` = %s;", (assignment.name, assignment.uidentifier, assignment.type, assignment.tutor.id, assignment.id))
        self.con.commit()
        cur.close()

    def del_assignment(self, assignment):
        cur = self.con.cursor()
        cur.execute("DELETE FROM `assignment` WHERE `id`=%s", (assignment.id,))
        self.con.commit()
        cur.close()

    def list_tutors(self):
        cur = self.con.cursor()
        cur.execute("SELECT `tutor`.`id`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `tutor` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` ORDER BY `tutor`.`id` ASC;")
        res = []
        for item in cur.fetchall():
            sub = Subject(id=item[3],
                          name=item[4],
                          desc=item[5],
                          uidentifier=item[6])
            teac = Tutor(id=item[0],
                         name=item[1],
                         uidentifier=item[2],
                         subject=sub)
            res.append(teac)
        cur.close()
        return res
        
    def get_tutor_by_uid(self, uid):
        # SELECT `tutor`.`id`, `tutor`.`name`, `tutor`.`uidentifier`, `subject`.`id`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `tutor` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` WHERE `uidentifier`=?;
        cur = self.con.cursor()
        cur.execute("SELECT `tutor`.`id`, `tutor`.`name`, `tutor`.`uidentifier`, `subject`.`id`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `tutor` JOIN `subject` ON `tutor`.`subid` = `subject`.`id` WHERE `tutor`.`uidentifier`=%s;", (uid,))
        item = cur.fetchone()
        if item:
            sub = Subject(id=item[3],
                          name=item[4],
                          desc=item[5],
                          uidentifier=item[6])
            teac = Tutor(id=item[0],
                         name=item[1],
                         uidentifier=item[2],
                         subject=sub)
        else:
            teac = None
        cur.close()
        return teac

    def add_tutor(self, tutor):
        cur = self.con.cursor()
        if tutor.id:
            cur.execute("INSERT INTO `tutor` (`id`, `name`, `uidentifier`, `subid`) VALUES (%s, %s, %s, %s)", (tutor.id, tutor.name, tutor.uidentifier, tutor.subject.id))
            self.con.commit()
        else:
            cur.execute("INSERT INTO `tutor` (`name`, `uidentifier`, `subid`) VALUES (%s, %s, %s)", (tutor.name, tutor.uidentifier, tutor.subject.id))
            self.con.commit()
            cur.execute("SELECT `id` FROM `tutor` WHERE `uidentifier`=%s LIMIT 1;", (tutor.uidentifier,))
            tutor.id = cur.fetchone()[0]
        cur.close()

    def edit_tutor(self, tutor):
        cur = self.con.cursor()
        cur.execute("UPDATE `tutor` SET `name`=%s, `uidentifier`=%s, `subid`=%s WHERE `id`=%s;", (tutor.name, tutor.uidentifier, tutor.subject.id, tutor.id))
        self.con.commit()
        cur.close()

    def delete_tutor(self, tutor):
        cur = self.con.cursor()
        cur.execute("DELETE FROM `tutor` WHERE `id`=%s", (tutor.id,))
        self.con.commit()
        cur.close()
        
    def get_tag_by_id(self, id, populate_parents=True):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor`, `tag`.`parent_tag_id` FROM `tag` WHERE `id`=%s LIMIT 1;", (id,))
        item = cur.fetchone()
        if item:
            if item[4] and populate_parents:
                parent = self.get_tag_by_id(item[4])
            else:
                parent = None
            tag = Tag(id=item[0],
                        text=item[1],
                        fgcolor=item[2],
                        bgcolor=item[3],
                        parent=parent)
            cur.close()
            return tag

    def list_tags(self, populate_parents=True):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor`, `tag`.`parent_tag_id` FROM `tag`;")
        res = []
        for item in cur.fetchall():
            if item[4] and populate_parents:
                parent = self.get_tag_by_id(item[4])
            else:
                parent = None
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3],
                      parent=parent)
            res.append(tag)
        cur.close()
        return res
        
    def search_tag_by_text_instr(self, text, populate_parents=True):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor`, `tag`.`parent_tag_id` FROM `tag` WHERE `tag`.`text` LIKE %s;", ("%"+text+"%",))
        res = []
        for item in cur.fetchall():
            if item[4] and populate_parents:
                parent = self.get_tag_by_id(item[4])
            else:
                parent = None
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3],
                      parent=parent)
            res.append(tag)
        cur.close()
        return res
        
    def get_tag(self, text, populate_parents=True):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor`, `tag`.`parent_tag_id` FROM `tag` WHERE `tag`.`text` = %s;", (text,))
        item = cur.fetchone()
        if item:
            if item[4] and populate_parents:
                parent = self.get_tag_by_id(item[4])
            else:
                parent = None
            tag = Tag(id=item[0],
                        text=item[1],
                        fgcolor=item[2],
                        bgcolor=item[3],
                        parent=parent)
        else:
            tag = None
        cur.close()
        return tag

    def add_tag(self, tag):
        cur = self.con.cursor()
        if tag.id:
            cur.execute("INSERT INTO `tag` (`id`, `text`, `fgcolor`, `bgcolor`, `parent_tag_id`) VALUES (%s, %s, %s, %s, %s);", (tag.id, tag.text, tag.fgcolor, tag.bgcolor, tag.parent.id if tag.parent else None))
            self.con.commit()
        else:
            cur.execute("INSERT INTO `tag` (`text`, `fgcolor`, `bgcolor`, `parent_tag_id`) VALUES (%s, %s, %s, %s);", (tag.text, tag.fgcolor, tag.bgcolor, tag.parent.id if tag.parent else None))
            self.con.commit()
            cur.execute("SELECT `id` FROM `tag` WHERE `text`=%s LIMIT 1;", (tag.text,))
            tag.id = cur.fetchone()[0]
        cur.close()

    def edit_tag(self, tag):
        cur = self.con.cursor()
        cur.execute("UPDATE `tag` SET `text`=%s, `fgcolor`=%s, `bgcolor`=%s, `parent_tag_id`=%s WHERE `id`=%s;", (tag.text, tag.fgcolor, tag.bgcolor, tag.parent.id if tag.parent else None, tag.id))
        self.con.commit()
        cur.close()

    def delete_tag(self, tag):
        cur = self.con.cursor()
        cur.execute("DELETE FROM `tag` WHERE `id`=%s;", (tag.id, ))
        self.con.commit()
        cur.close()

    def tag_assignment(self, assignment, tag):
        cur = self.con.cursor()
        cur.execute("INSERT INTO `assignment_tag` (`assignment_id`, `tag_id`) VALUES (%s, %s);", (assignment.id, tag.id))
        self.con.commit()
        cur.close()

    def untag_assignment(self, assignment, tag):
        cur = self.con.cursor()
        cur.execute("DELETE FROM `assignment_tag` WHERE `assignment_id` = %s AND `tag_id` = %s;", (assignment.id, tag.id))
        self.con.commit()
        cur.close()
        
    def assignment_tags(self, assignment, populate_parents=True):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor`, `tag`.`parent_tag_id` FROM `assignment`, `assignment_tag`, `tag` WHERE `assignment`.`id` = `assignment_tag`.`assignment_id` AND `assignment_tag`.`tag_id` = `tag`.`id` AND `assignment`.`id` = %s;", (assignment.id,))
        res = []
        for item in cur.fetchall():
            if item[4] and populate_parents:
                parent = self.get_tag_by_id(item[4])
            else:
                parent = None
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3],
                      parent=parent)
            res.append(tag)
        cur.close()
        return res
        
    def tagged_assignments(self, tag):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subid`, `subject`.`name`, `subject`.`desc`, `subject`.`uidentifier` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `subject` ON `subject`.`id` = `tutor`.`subid` JOIN `assignment_tag` ON `assignment`.`id` = `assignment_tag`.`assignment_id` JOIN `tag` ON `assignment_tag`.`tag_id` = `tag`.`id` WHERE `tag`.`id` = %s;", (tag.id,))
        res = []
        for item in cur.fetchall():
            sub = Subject(id=item[7],
                          name=item[8],
                          desc=item[9],
                          uidentifier=item[10])
            teac = Tutor(id=item[4],
                         name=item[5],
                         uidentifier=item[6],
                         subject=sub)
            ass = Assignment(id=item[0],
                             name=item[1],
                             uidentifier=item[2],
                             type=item[3],
                             tutor=teac)
            res.append(ass)
        cur.close()
        return res

    def sql_query(self):
        raise NotImplementedError

