import tkinter as tk
from tkinter import ttk
import pymysql

from gurutracker.config import settings
from gurutracker.views.mainwindow import MainWindow
from gurutracker.database import mysql, sqlite3
import gurutracker.helpers.excdialog

__version__ = "0.2.0"
__db_revision__ = "3"
__gxp_version__ = "1.0.1"

def main():
    if settings.get("database", "type") == "mysql":
        conn = pymysql.connect(host=settings.get("database", "host"),
            port=settings.getint("database", "port"),
            user=settings.get("database", "user"),
            password=settings.get("database", "password"),
            database=settings.get("database", "database"))
        controller = mysql.Controller(conn)
    elif settings.get("database", "type") == "sqlite3":
        conn = settings.get("database", "file")
        controller = sqlite3.Controller(conn)
    else:
        raise TypeError("no such database type, please see docs")
    
    tk.Tk.report_callback_exception = gurutracker.helpers.excdialog.show_error
    
    win = MainWindow(controller)
    # theming
    # style = ttk.Style()
    # win.tk.call("source", "themes/azure/light.tcl")
    # style.theme_use("azure-light")
    # theming end
    win.mainloop()
    
