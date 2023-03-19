# to discover config files
import os

CFG_LOCATIONS = ["configuration.ini",
                 "~/.gurutracker/configuration.ini"]

def get_config_loc():
    ret = os.path.expanduser(CFG_LOCATIONS[-1])
    for i in CFG_LOCATIONS:
        if os.path.isfile(os.path.expanduser(i)):
            ret = os.path.expanduser(i)
    return ret