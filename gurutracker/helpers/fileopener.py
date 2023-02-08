import os


def filepath(config, uid):
    return '.'.join((os.path.join(os.path.join(*config.get("files", "datadir").split("/")), os.path.join(*uid.split("/"))), config.get("files", "extension")))

def dirpath(config, uid):
    return os.path.join(os.path.join(*config.get("files", "datadir").split("/")), os.path.join(*(uid.split("/")[:-1])))

def valid_filepath(config, uid):
    return os.path.isfile(filepath(config, uid))
