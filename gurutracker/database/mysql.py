import pymysql

from gurutracker.database.base import Base
from gurutracker.database.objects import Tutor, Assignment, Tag

class Controller(Base):
    def __init__(self, connection):
        self.con = connection
        
    def list_all_assignments(self):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` ORDER BY `assignment`.`id` ASC;")
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

    def list_all_assignments_customsql(self, custom_sql):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id`" + custom_sql + ";")
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
        
    def get_assignment_by_id(self, id):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment`, `tutor` WHERE `assignment`.`tid` = `tutor`.`id` AND `assignment`.`id` = %s LIMIT 1;", (id,))
        item = cur.fetchone()
        if item:
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
            cur.close()
            return ass
    
    def get_assignment_by_uid(self, uid):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment`, `tutor` WHERE `assignment`.`tid` = `tutor`.`id` AND `assignment`.`uidentifier` = %s LIMIT 1;", (uid,))
        item = cur.fetchone()
        if item:
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
        raise NotImplementedError

    def list_tutors(self):
        cur = self.con.cursor()
        cur.execute("SELECT `tutor`.`id`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `tutor`;")
        res = []
        for item in cur.fetchall():
            teac = Tutor(id=item[0],
                         name=item[1],
                         uidentifier=item[2],
                         subject=item[3],
                         level=item[4])
            res.append(teac)
        cur.close()
        return res
        
    def get_tutor_by_uid(self, uid):
        raise NotImplementedError

    def add_tutor(self, tutor):
        raise NotImplementedError

    def edit_tutor(self, tutor):
        raise NotImplementedError

    def delete_tutor(self, tutor):
        raise NotImplementedError

    def list_tags(self):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor` FROM `tag`;")
        res = []
        for item in cur.fetchall():
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3])
            res.append(tag)
        cur.close()
        return res
        
    def search_tag_by_text_instr(self, text):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor` FROM `tag` WHERE `tag`.`text` LIKE %s;", ("%"+text+"%",))
        res = []
        for item in cur.fetchall():
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3])
            res.append(tag)
        cur.close()
        return res
        
    def get_tag(self, text):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor` FROM `tag` WHERE `tag`.`text` = %s;", (text,))
        item = cur.fetchone()
        if item:
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3])
        else:
            tag = None
        cur.close()
        return tag

    def add_tag(self, tag):
        cur = self.con.cursor()
        cur.execute("INSERT INTO `tag` (`text`, `fgcolor`, `bgcolor`) VALUES (%s, %s, %s);", (tag.text, tag.fgcolor, tag.bgcolor))
        self.con.commit()
        cur.execute("SELECT `id` FROM `tag` WHERE `text`=%s LIMIT 1;", (tag.text,))
        tag.id = cur.fetchone()[0]
        cur.close()

    def edit_tag(self, tag):
        raise NotImplementedError

    def delete_tag(self, tag):
        raise NotImplementedError

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
        
    def assignment_tags(self, assignment):
        cur = self.con.cursor()
        cur.execute("SELECT `tag`.`id`, `tag`.`text`, `tag`.`fgcolor`, `tag`.`bgcolor` FROM `assignment`, `assignment_tag`, `tag` WHERE `assignment`.`id` = `assignment_tag`.`assignment_id` AND `assignment_tag`.`tag_id` = `tag`.`id` AND `assignment`.`id` = %s;", (assignment.id,))
        res = []
        for item in cur.fetchall():
            tag = Tag(id=item[0],
                      text=item[1],
                      fgcolor=item[2],
                      bgcolor=item[3])
            res.append(tag)
        cur.close()
        return res
        
    def tagged_assignments(self, tag):
        cur = self.con.cursor()
        cur.execute("SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `assignment_tag` ON `assignment`.`id` = `assignment_tag`.`assignment_id` JOIN `tag` ON `assignment_tag`.`tag_id` = `tag`.`id` WHERE `tag`.`id` = %s;", (tag.id,))
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

    def sql_query(self):
        raise NotImplementedError
"""
SELECT `assignment`.`id`, `assignment`.`name`, `assignment`.`uidentifier`, `assignment`.`type`, `assignment`.`tid`, `tutor`.`name`, `tutor`.`uidentifier`, `tutor`.`subject`, `tutor`.`level`, `tag`.`text` FROM `assignment` JOIN `tutor` ON `assignment`.`tid` = `tutor`.`id` JOIN `assignment_tag` ON `assignment`.`id` = `assignment_tag`.`assignment_id` JOIN `tag` ON `assignment_tag`.`tag_id` = `tag`.`id`;
"""
