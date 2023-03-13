import csv
import os
import json
import shutil
import tempfile
import zipfile

import gurutracker
from gurutracker.globals import settings as config, controller
from gurutracker.helpers.fileopener import filepath, valid_filepath



class VersionMismatchError(Exception):
    pass


def _zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file), 
                       os.path.relpath(os.path.join(root, file), 
                                       path))
            

def zip_directory(src, dst):
    with zipfile.ZipFile(dst, 'w', zipfile.ZIP_DEFLATED) as zipf:
        _zipdir(src, zipf)


def export(output):
    # Create temp dir
    tempdir = tempfile.TemporaryDirectory()
    
    cur = controller.con.cursor()

    # Version info
    with open(os.path.join(tempdir.name, "version"), "w") as fp:
        json.dump({
                "gurutracker_version": gurutracker.__version__,
                "database_version": gurutracker.__db_revision__,
                "gxp_version": gurutracker.__gxp_version__,
            }, fp)
        
    # Notes
    if config.getboolean("notes", "enabled"):
        shutil.copy(config.get("notes", "textfile"), os.path.join(tempdir.name, "notes"))
    
    # SQL data
    with open(os.path.join(tempdir.name, "tutors.csv"), "w", newline="") as fp:
        writer = csv.writer(fp)
        cur.execute("SELECT `id`, `name`, `uidentifier`, `subject`, `level` FROM `tutor`;")
        writer.writerows(cur.fetchall())
        
    with open(os.path.join(tempdir.name, "assignments.csv"), "w", newline="") as fp:
        writer = csv.writer(fp)
        cur.execute("SELECT `id`, `name`, `uidentifier`, `type`, `tid` FROM `assignment`;")
        writer.writerows(cur.fetchall())
    
    os.mkdir(os.path.join(tempdir.name, "tag"))
    
    with open(os.path.join(tempdir.name, "tag", "tagdata.csv"), "w", newline="") as fp:
        writer = csv.writer(fp)
        cur.execute("SELECT `id`, `text`, `fgcolor`, `bgcolor` FROM `tag`;")
        writer.writerows(cur.fetchall())
    
    with open(os.path.join(tempdir.name, "tag", "tagmapping.csv"), "w", newline="") as fp:
        writer = csv.writer(fp)
        cur.execute("SELECT `assignment_id`, `tag_id` FROM `assignment_tag`;")
        writer.writerows(cur.fetchall())
    
    
    
    # files
    os.mkdir(os.path.join(tempdir.name, "files"))
    cur.execute("SELECT `assignment`.`id`, `assignment`.`uidentifier` FROM `assignment`;")
    
    for id, uid in cur.fetchall():
        if valid_filepath(config, uid):
            shutil.copy(filepath(config, uid), 
                        os.path.join(tempdir.name, 
                                     "files", 
                                     "file_{:04d}.{}".format(id, 
                                                             config.get("files", "extension")) ))
    
    # copy and cleanup
    """
    shutil.make_archive(output, "zip", tempdir.name)
    os.rename(output+".zip", output)
    """
    zip_directory(tempdir.name, output)
    cur.close()
    tempdir.cleanup()


def import_(ifile):
    tempdir = tempfile.TemporaryDirectory()
    
    d = "%s" if config.get("database", "type") == "mysql" else "?"
    
    with zipfile.ZipFile(ifile) as zf:
        zf.extractall(tempdir.name)
    
    f1 = open(os.path.join(tempdir.name, "tutors.csv"), "r", newline="")
    f2 = open(os.path.join(tempdir.name, "assignments.csv"), "r", newline="")
    f3 = open(os.path.join(tempdir.name, "tag", "tagdata.csv"), "r", newline="")
    f4 = open(os.path.join(tempdir.name, "tag", "tagmapping.csv"), "r", newline="")
    cur = controller.con.cursor()
    
    try:
        if os.path.isfile(os.path.join(tempdir.name, "version")):
            with open(os.path.join(tempdir.name, "version"), "r") as fp:
                data = json.load(fp)
        else:
            data = {"gxp_version": None}
        
        if data["gxp_version"] != gurutracker.__gxp_version__:
            raise VersionMismatchError
        
        if os.path.isfile(os.path.join(tempdir.name, "notes")):
            shutil.copy(os.path.join(tempdir.name, "notes"), config.get("notes", "textfile"))
    
        for item in csv.reader(f1):
            cur.execute(f"INSERT INTO `tutor` (`id`, `name`, `uidentifier`, `subject`, `level`) VALUES ({d}, {d}, {d}, {d}, {d});",
                        (int(item[0]), item[1], item[2], item[3], item[4]))
            controller.con.commit()
        
        for item in csv.reader(f2):
            cur.execute(f"INSERT INTO `assignment` (`id`, `name`, `uidentifier`, `type`, `tid`) VALUES ({d}, {d}, {d}, {d}, {d});",
                        (int(item[0]), item[1], item[2], item[3], int(item[4])))
            controller.con.commit()
            
        for item in csv.reader(f3):
            cur.execute(f"INSERT INTO `tag` (`id`, `text`, `fgcolor`, `bgcolor`) VALUES ({d}, {d}, {d}, {d});",
                        (int(item[0]), item[1], item[2], item[3]))
            controller.con.commit()
            
        for item in csv.reader(f4):
            if item[0] and item[1]:
                cur.execute(f"INSERT INTO `assignment_tag` (`assignment_id`, `tag_id`) VALUES ({d}, {d});",
                            (int(item[0]), int(item[1]),))
                controller.con.commit()
    finally:
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        cur.close()
        tempdir.cleanup()
    
    # cur.execute("SELECT `assignment`.`id`, `assignment`.`uidentifier` FROM `assignment`;")
    
    """
    for id, uid in cur.fetchall():
        if valid_filepath(config, uid):
            shutil.copy(filepath(config, uid), 
                        os.path.join(tempdir.name, 
                                     "files", 
                                     "file_{:04d}.{}".format(id, 
                                                             config.get("files", "extension")) ))"""
