"""Storage Helpers

This module deals with storage helpers for unzipping
"""

import os
import subprocess
import tempfile
import atexit
import webbrowser

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
    for file in opened_files:
        os.unlink(file)