"""Storage Helpers

This module deals with storage helpers for unzipping
"""

import os
import tempfile
import atexit
import webbrowser

opened_files = []

def open_file(fp):
    """open_file 
    
    Open a file

    Args:
        fp (ReadableBuffer): 
            The file pointer (in rb mode) with .ext attribute
    """
    tf = tempfile.NamedTemporaryFile(mode="wb", suffix=f".{fp.ext}", delete=False)
    tf.write(fp.read())
    tf.close()
    webbrowser.open_new(tf.name)
    opened_files.append(tf)

@atexit.register
def delete_all():
    for file in opened_files:
        os.unlink(file.name)