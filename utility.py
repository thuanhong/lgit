import os
from hashlib import sha1
from datetime import datetime


def write_file(name_file, content, mode):
    """
    write content into file
    @param name_file : file name
    @param content : Content will be written to the file
    @param mode : methods (modes) for opening a file
    @return None
    """
    file = open(name_file, mode)
    file.write(content)
    file.close()


def fatal_error():
    """
    catch error if the program execute commands as : add, status, ...
    without folder init
    @param None
    @return True if lgit have a fatal error, otherwise return False
    """
    if not os.path.exists('.lgit'):
        print("Reinitialized existing Git repository in " + os.getcwd())
        return True
    return False


def get_timestamp(file_name):
    """
    get last modify time of file or directory
    @param file_name : name of file or directory
    @return timestamps of file
    """
    mod_time = os.stat(file_name).st_mtime
    return datetime.fromtimestamp(mod_time).strftime("%Y%m%d%H%M%S")


def get_sha1(file_name):
    """
    get SHA1 hash of content file
    @param file_name : file name
    @return None
    """
    file = open(file_name, 'r')
    code_sha1 = sha1(file.read().encode()).hexdigest()
    file.close()
    return code_sha1
