"""Load from Old

This helps in loading from old GXP versions to the system.
"""

import csv
import sys
import json
import os
import shutil
import tempfile
import zipfile

from gurutracker.database.objects import Subject, Tutor, Assignment, Tag
from gurutracker.globals import settings, controller, storage
from gurutracker.helpers.excdialog import errstr
from gurutracker.helpers.appdata.exceptions import VersionMismatchError


def load_from_v1(file_path, stream=sys.stdout):
    """load_from_v1 
    
    Load GXP of Version 1.x.x

    Args:
        file_path (str): File path
        stream (StringIO): 
            A file-like object with .write() method - to write progress
    """
    tempdir = tempfile.TemporaryDirectory()
    
    with zipfile.ZipFile(file_path) as zf:
        zf.extractall(tempdir.name)
    
    f1 = open(os.path.join(tempdir.name, "tutors.csv"), "r", newline="")
    f2 = open(os.path.join(tempdir.name, "assignments.csv"), "r", newline="")
    f3 = open(os.path.join(tempdir.name, "tag", "tagdata.csv"), "r", newline="")
    f4 = open(os.path.join(tempdir.name, "tag", "tagmapping.csv"), "r", newline="")
    
    stream.write("[0] Opened file and finished extraction. File objects open.\n")
    
    try:
        if os.path.isfile(os.path.join(tempdir.name, "version")):
            with open(os.path.join(tempdir.name, "version"), "r") as fp:
                data = json.load(fp)
        else:
            data = {"gxp_version": "0.0.0"}
        
        if data["gxp_version"].split(".")[0] != "1":
            stream.write("[E,VM] Cannot handle this version\n")
            raise VersionMismatchError
        
        if os.path.isfile(os.path.join(tempdir.name, "notes")):
            shutil.copy(os.path.join(tempdir.name, "notes"), os.path.expanduser(settings.get("notes", "textfile")))
        
        stream.write("[1] Copied notes file\n")
            
        # Get Subjects
        subjects = {}
        for item in csv.reader(f1):
            subjects[item[3]] = None
        
        for subname in subjects:
            sub = Subject(name=subname,
                          desc=("Imported automatically by Gurutracker."
                                " Feel free to modify this description."),
                          uidentifier=subname.upper())
            controller.add_subject(sub)
            subjects[subname] = sub
        
        stream.write("[2] Copied subjects\n")
        
        f1.seek(0)
        
        for item in csv.reader(f1):
            tut = Tutor(id=int(item[0]),
                        name="{} ({})".format(item[1], item[4]),
                        uidentifier=item[2].upper(),
                        subject=subjects[item[3]])
            controller.add_tutor(tut)
        
        stream.write("[3] Copied tutors\n")
        
        for item in csv.reader(f2):
            ass = Assignment(id=int(item[0]),
                             name=item[1],
                             uidentifier="/".join(item[2].split("/")[2:]).upper(),
                             type=item[3],
                             tutor=Tutor(
                                 id=int(item[4])
                             ))
            controller.add_assignment(ass)
        
        stream.write("[3] Copied assignments\n")
            
        for item in csv.reader(f3):
            ta = Tag(id=int(item[0]),
                     text=item[1],
                     fgcolor=item[2],
                     bgcolor=item[3])
            controller.add_tag(ta)
        
        stream.write("[4] Copied tags\n")
            
        for item in csv.reader(f4):
            if item[0] and item[1]:
                controller.tag_assignment(
                    Assignment(id=int(item[0])),
                    Tag(id=int(item[1]))
                )
        
        stream.write("[5] Linked tags with assignments\n")
        
        asl = controller.list_all_assignments()
        for ass in asl:
            if os.path.isfile(os.path.join(tempdir.name, "files", 
                    "file_{:04d}.{}".format(ass.id, settings.get("files", "extension", fallback="pdf")))):
                f = open(os.path.join(tempdir.name, "files", 
                    "file_{:04d}.{}".format(ass.id, settings.get("files", 
                    "extension", fallback="pdf"))), "rb")
                f.ext = settings.get("files", "extension", fallback="pdf")
                storage.link_file(f, ass)
                f.close()
        
        stream.write("[6] Linked files with assignment\n")
    except Exception as e:
        stream.write("[E] An exception occured.\n{}".format(errstr(e)))
    else:
        stream.write("[D] Done\n")
    finally:
        f1.close()
        f2.close()
        f3.close()
        f4.close()
        tempdir.cleanup()
    
    # cur.execute("SELECT `assignment`.`id`, `assignment`.`uidentifier` FROM `assignment`;")
    
    """
    for id, uid in cur.fetchall():
        if valid_filepath(settings, uid):
            shutil.copy(filepath(settings, uid), 
                        os.path.join(tempdir.name, 
                                     "files", 
                                     "file_{:04d}.{}".format(id, 
                                                             settings.get("files", "extension")) ))"""
