"""
file used to print all file have neen added
"""
import os
from os import getcwd
from utility import set_path, fatal_error


def ls_files():
    dir_name = getcwd().split('/')[-1]
    dir_script = os.path.basename(os.path.dirname(__file__))
    set_path(__file__)
    fatal_error()
    file_index = open('.lgit/index')
    if dir_name != dir_script:
        for line in sorted(file_index, key=len):
            path = line.split()[-1].split('/')
            start = path.index(dir_name)
            print(*path[start+1:], sep='/')
        return

    for line in sorted(file_index, key=len):
        print(line.split()[-1])
    file_index.close()
