import os

from gurutracker.config.py_configparser import Config
from gurutracker.database import mysql, sqlite3 as sqlite

if "GURUTRACKER_CONFIGURATION_TESTING" in os.environ:
    settings = Config("testing.ini")
else:
    settings = Config()
settings.read_config()

if settings.get("database", "type") == "mysql":
    import pymysql
    conn = pymysql.connect(host=settings.get("database", "host"),
        port=settings.getint("database", "port"),
        user=settings.get("database", "user"),
        password=settings.get("database", "password"),
        database=settings.get("database", "database"))
    controller = mysql.Controller(conn)
elif settings.get("database", "type") == "sqlite3":
    import sqlite3
    conn = sqlite3.connect(settings.get("database", "file"))
    controller = sqlite.Controller(conn)
else:
    raise TypeError("no such database type, please see docs")