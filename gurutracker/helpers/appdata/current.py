import csv
import sys
import json
import os
import shutil
import tempfile
import zipfile

import gurutracker
from gurutracker.database.objects import Subject, Tutor, Assignment, Tag
from gurutracker.globals import settings, controller, storage
from gurutracker.helpers.excdialog import errstr
from gurutracker.helpers.appdata.exceptions import VersionMismatchError
from gurutracker.helpers.appdata.common import zip_directory


def dump_v2_0(file_path, stream=sys.stdout):
    """dump_v2_0
    
    Dump GXP of Version 2.0.x

    Args:
        file_path (str): File path
        stream (StringIO): 
            A file-like object with .write() method - to write progress
    """
    stream.write("[I] Number of steps: 010\n")
    
    tempdir = tempfile.TemporaryDirectory()
    
    try:
        f0 = open(os.path.join(tempdir.name, "version"), "w")
        json.dump({
                "gurutracker_version": gurutracker.__version__,
                "database_version": gurutracker.__db_revision__,
                "gxp_version": gurutracker.__gxp_version__,
        }, f0)
        f0.close()
        stream.write("[001] Written version string\n")
        
        
        # Notes
        stream.write("[*] Checking for notes...\n")
        if settings.getboolean("notes", "enabled"):
            shutil.copy(os.path.expanduser(settings.get("notes", "textfile")), 
                        os.path.join(tempdir.name, "notes"))
            stream.write("[002] Copied notes file\n")
        else:
            stream.write("[002] Notes disabled.\n")
        
        os.mkdir(os.path.join(tempdir.name, "data"))
        stream.write("[003] Created data folder\n")
        
        stream.write("[*] Starting to copy subjects\n")
        f1 = open(os.path.join(tempdir.name, "data", "subject.csv"), "w", newline="")
        w1 = csv.writer(f1)
        for sub in controller.list_all_subjects():
            w1.writerow([sub.id, sub.name, sub.desc, sub.uidentifier])
            # stream.write(f"[*] Copied subject {sub.id}\n")
        stream.write("[004] Copied subjects\n")
        f1.close()
        
        # copy tutors
        stream.write("[*] Starting to copy tutors\n")
        f1 = open(os.path.join(tempdir.name, "data", "tutor.csv"), "w", newline="")
        w1 = csv.writer(f1)
        for tut in controller.list_tutors():
            w1.writerow([tut.id, tut.name, tut.uidentifier, tut.subject.id])
            # stream.write(f"[*] Copied tutor {tut.id}\n")
        stream.write("[005] Copied tutors\n")
        f1.close()
        
        # copy assignments
        stream.write("[*] Starting to copy assignments\n")
        f1 = open(os.path.join(tempdir.name, "data", "assignment.csv"), "w", newline="")
        w1 = csv.writer(f1)
        for ass in controller.list_all_assignments():
            w1.writerow([ass.id, ass.name, ass.uidentifier, ass.type, ass.tutor.id])
            # stream.write(f"[*] Copied assignment {ass.id}\n")
        stream.write("[006] Copied assignments\n")
        f1.close()
        
        # copy tags
        stream.write("[*] Starting to copy tags\n")
        f1 = open(os.path.join(tempdir.name, "data", "tag.csv"), "w", newline="")
        w1 = csv.writer(f1)
        for tag in controller.list_tags():
            w1.writerow([tag.id, tag.text, tag.fgcolor, tag.bgcolor, tag.parent.id if tag.parent else ""])
            # stream.write(f"[*] Copied tag {tag.id}\n")
        stream.write("[007] Copied tags\n")
        f1.close()
        
        # copy tag assignment relations
        stream.write("[*] Starting to copy tag assignment relations\n")
        f1 = open(os.path.join(tempdir.name, "data", "assignment_tag.csv"), "w", newline="")
        w1 = csv.writer(f1)
        for ass in controller.list_all_assignments():
            for tag in controller.assignment_tags(ass, populate_parents=False):
                w1.writerow([ass.id, tag.id])
                # stream.write(f"[*] Copied tag {tag.id}\n")
        stream.write("[008] Copied tag assignment relations\n")
        f1.close()
        
        # Starting to copy files
        os.mkdir(os.path.join(tempdir.name, "files"))
        stream.write("[*] Starting to copy files\n")
        fi = open(os.path.join(tempdir.name, "files", "file_extensions.csv"), "w", newline="")
        cs = csv.writer(fi)
        asl = controller.list_all_assignments()
        for ass in asl:
            if storage.has_linked_file(ass):
                src = storage.get_file(ass)
                dst = open(os.path.join(tempdir.name, "files", "file_{:04d}".format(ass.id)), "wb")
                dst.write(src.read())
                dst.close()
                src.close()
                cs.writerow([ass.id, src.ext])
        fi.close()
        stream.write("[009] Finished copying files\n")
        
        zip_directory(tempdir.name, file_path)
        stream.write("[010] Finished zipping files\n")
    except Exception as e:
        stream.write("[E] An exception occured.\n{}".format(errstr(e)))
    else:
        stream.write("[D] Done\n")
    finally:
        tempdir.cleanup()
    

