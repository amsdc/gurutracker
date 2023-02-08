import tkinter as tk
from tkinter import ttk
import pymysql

from gurutracker.config.py_configparser import Config
from gurutracker.views.mainwindow import MainWindow
from gurutracker.database import mysql, sqlite3
import gurutracker.helpers.excdialog

__version__ = "0.2.0"
__db_revision__ = "3"
__gxp_version__ = "1.0.1"

def main():
    config = Config()
    config.read_config()

    if config.get("database", "type") == "mysql":
        conn = pymysql.connect(host=config.get("database", "host"),
            port=config.getint("database", "port"),
            user=config.get("database", "user"),
            password=config.get("database", "password"),
            database=config.get("database", "database"))
        controller = mysql.Controller(conn)
    elif config.get("database", "type") == "sqlite3":
        conn = config.get("database", "file")
        controller = sqlite3.Controller(conn)
    else:
        raise TypeError("no such database type, please see docs")
    
    tk.Tk.report_callback_exception = gurutracker.helpers.excdialog.show_error
    
    win = MainWindow(config, controller)
    # theming
    # style = ttk.Style()
    # win.tk.call("source", "themes/azure/light.tcl")
    # style.theme_use("azure-light")
    # theming end
    win.mainloop()
    
