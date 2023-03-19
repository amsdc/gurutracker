import os

from gurutracker.config.py_configparser import Config
from gurutracker.config.discoverer import get_config_loc
from gurutracker.database import mysql, sqlite3 as sqlite
from gurutracker.storage import filesystem

if "GURUTRACKER_CONFIGURATION_TESTING" in os.environ:
    settings = Config("testing.ini")
else:
    settings = Config(get_config_loc())
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
    dire = os.path.expanduser(settings.get("database", "file"))
    conn = sqlite3.connect(dire)
    controller = sqlite.Controller(conn)
    del dire
else:
    raise TypeError("no such database type, please see docs")

# storage adapter cfg
if settings.get("storage", "type") == "filesystem.directory":
    dire = os.path.expanduser(settings.get("storage", "directory"))
    if not os.path.isdir(dire):
        os.makedirs(dire)
    storage = filesystem.FilesystemDirectory(dire)
    del dire
else:
    raise TypeError("no such storage type, please see docs")

# icon dir
module_path = os.path.dirname(__file__)