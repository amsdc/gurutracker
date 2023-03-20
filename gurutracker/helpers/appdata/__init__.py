import json
import os
import zipfile

from gurutracker import __gxp_version__
from gurutracker.globals import settings, controller


def versionstr_to_tuple(vesrionstr):
    return tuple(map(int, vesrionstr.split(".")))


def is_compatible(version1, version2=__gxp_version__):
    """is_compatible 
    
    Tell if two versions are compatible as per the Semantic Versioning 
    standard.

    Args:
        version1 (str): Version to compare
        version2 (str, optional): 
            Version of software. Defaults to __gxp_version__.

    Returns:
        bool: True if versions are compatible
    """
    v1 = versionstr_to_tuple(version1)
    v2 = versionstr_to_tuple(version2)
    
    return v1[0] == v2[0] and v1[1] <= v2[1]


def get_gxp_version(ifile):
    with zipfile.ZipFile(ifile) as zf:
        with zf.open("version", "r") as vf:
            return json.load(vf)


def should_use_converter(ifile):
    """should_use_converter 
    
    Judge if a GXP file should use the converter.

    Args:
        ifile (str): Input file
    """
    ver1 = get_gxp_version(ifile)
    v1 = versionstr_to_tuple(ver1["gxp_version"])
    v2 = versionstr_to_tuple(__gxp_version__)
    return v1[0] < v2[0]

def get_converter_name(ifile):
    """should_use_converter 
    
    Get converter name to import from
    `gurutracker.helpers.appdata.load_from_old` Use `getattr` to get 
    the function.

    Args:
        ifile (str): Input file
    """
    ver1 = get_gxp_version(ifile)
    v = versionstr_to_tuple(ver1["gxp_version"])
    if v[0] == 1:
        return "load_from_v1"


def check_loadable():
    """check_if_importable 
    
    Check if the database and notes are empty so that data can be 
    imported.
    
    Returns:
        bool: True if data is importable
    """
    return (
        len(controller.list_all_subjects()) == 0
        and len(controller.list_tutors()) == 0
        and len(controller.list_all_assignments()) == 0
        and not os.path.isfile(os.path.expanduser("notes", "textfile"))
    )