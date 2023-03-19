"""Storage Helpers

This module deals with storage helpers for unzipping
"""

import os
import subprocess
import tempfile
import atexit
import webbrowser

from gurutracker.globals import settings

opened_files = []

def _save_file(fp):
    """open_file 
    
    Open a file handle

    Args:
        fp (ReadableBuffer): 
            The file pointer (in rb mode) with .ext attribute
    """
    tf = tempfile.NamedTemporaryFile(mode="wb", suffix=f".{fp.ext}", delete=False)
    tf.write(fp.read())
    tf.close()
    opened_files.append(tf.name)
    return tf.name


def open_file(fp):
    """open_file 
    
    Open a file

    Args:
        fp (ReadableBuffer): 
            The file pointer (in rb mode) with .ext attribute
    """
    webbrowser.open_new(_save_file(fp))


def send_file(fp, to):
    subprocess.Popen([os.path.expanduser(os.path.join(
        "~/AppData/Roaming/Microsoft/Windows/SendTo", to)), _save_file(fp)], shell=True)


@atexit.register
def delete_all():
    l = []
    if os.path.isfile(os.path.expanduser(settings.get("storage", "tempinfo"))):
        fp = open(os.path.expanduser(settings.get("storage", "tempinfo")), "r")
        l = fp.read().strip().split()
    tp = tempfile.TemporaryFile("w+")
    for file in (opened_files + l):
        try:
            os.unlink(file)
        except:
            tp.write(file+"\n")
    if os.path.isfile(os.path.expanduser(settings.get("storage", "tempinfo"))):
        fp.close()
    
    tp.seek(0)
    fp = open(os.path.expanduser(settings.get("storage", "tempinfo")), "w")
    fp.write(tp.read())
    tp.close()
    fp.close()