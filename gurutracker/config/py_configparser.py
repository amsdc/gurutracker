import configparser
import csv
import functools
import os

from gurutracker.config.constants import SETTINGS_FILE_NAME, DEFAULT_SETTINGS


class Config():
    config = configparser.ConfigParser
    
    def __init__(self, filename=SETTINGS_FILE_NAME):
        self.filename = filename
        
        self.config = configparser.ConfigParser()
        self.config.read_dict(DEFAULT_SETTINGS)
        
        self.get = self.config.get
        self.set = self.config.set
        self.getint = self.config.getint
        self.getfloat = self.config.getfloat
        self.getboolean = self.config.getboolean
        
    def getlist(self, *a, **kw):
        cols2show = self.config.get(*a, **kw)
        return next(csv.reader([cols2show], skipinitialspace=True))
        
    def write(self):
        with open(self.filename, "w") as f:
            self.config.write(f)

    def _read_config(self):
        self.config.read(self.filename)

    def read_config(self):
        if not os.path.isfile(self.filename):
            self.write()
        self._read_config()
