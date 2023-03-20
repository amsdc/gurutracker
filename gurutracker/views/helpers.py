import os
import shutil
from tkinter import messagebox
from tkinter import filedialog

# import gurutracker.helpers.fileopener

def center_window(win):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

def center_window_wrt(win, wrt):
    """
    centers a tkinter window
    :param win: the main window or Toplevel window to center
    """
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = wrt.winfo_rootx() + (wrt.winfo_width() - win_width) // 2
    y = wrt.winfo_rooty() #+ (wrt.winfo_height() - win_height) // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()
    
# def associate_file_with_record(config, selected_record, fname):
#     if gurutracker.helpers.fileopener.valid_filepath(config, selected_record.uidentifier):
#         if not messagebox.askyesno("Warning", "A file is already present. This will OVERWRITE the file. Proceed?"):
#             return

#     if fname:
#         path = gurutracker.helpers.fileopener.filepath(config, selected_record.uidentifier)
#         os.makedirs(os.path.split(path)[0], exist_ok=True)
#         shutil.copy(fname, path)
#         messagebox.showinfo("Success", "Success. Please refresh to open file")
#         return True