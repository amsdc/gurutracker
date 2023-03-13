import tkinter as tk
from tkinter import ttk

from gurutracker.views.mainwindow import MainWindow
import gurutracker.helpers.excdialog

__version__ = "0.2.0"
__db_revision__ = "3"
__gxp_version__ = "1.0.1"

def main():
    tk.Tk.report_callback_exception = gurutracker.helpers.excdialog.show_error
    
    win = MainWindow()
    # theming
    # style = ttk.Style()
    # win.tk.call("source", "themes/azure/light.tcl")
    # style.theme_use("azure-light")
    # theming end
    win.mainloop()
    
