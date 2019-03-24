"""
file support all another files
contain sub function
"""
import os
from hashlib import sha1
from datetime import datetime


def set_path(file):
    """
    change directory working
    """
    os.chdir(os.path.dirname(os.path.realpath(file)))


def write_file(name_file, content, mode):
    """
    rewrite/append content into file
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
    path = os.path.dirname(os.path.realpath(__file__)) + '/.lgit'
    if not os.path.exists(path):
        print("fatal: not a git repository (or any of the parent directories)")
        quit()


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


def check_file(file_name):
    """
    print error if file not exist
    """
    if not os.path.exists(file_name):
        print("fatal: pathspec '" + file_name + "' did not match any files")
        quit()


def get_path(file_name):
    """
    take file path from file name
    the path will start from directory run python script
    """
    # get dir name contain script running
    dir = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    file_path = os.path.realpath(file_name).split('/')
    try:
        start = file_path.index(dir) + 1
        return "/".join(file_path[start:])
    except IndexError:
        return file_name


def get_path_recursive(list_path, list_add, dir=''):
    '''
    handle recursive when add directory and more
    @param list_add : all file need add
    @return None
    '''
    for element in list_add:
        element = dir + element
        if os.path.isdir(element):
            get_path_recursive(list_path, os.listdir(element), element + '/')
        else:
            list_path.append(get_path(element))


def change_hash(pos, content):
    """
    write content in file line by line
    @param pos : position start write
    @param content : the content need write
    @return None
    """
    file = os.open('.lgit/index', os.O_RDWR)
    os.lseek(file, pos, 0)
    os.write(file, content.encode())
    os.close(file)
