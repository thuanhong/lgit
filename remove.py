from os import unlink
import os
from utility import check_file, get_path, set_path


def rm(file_name):
    check_file(file_name)

    file_name = get_path(file_name)
    set_path(__file__)
    file = open('.lgit/index', 'r')
    output = []
    for line in file:
        if line.split()[-1] != file_name:
            output.append(line)
    file.close()
    file = open('.lgit/index', 'w')
    file.writelines(output)
    file.close()
    unlink(file_name)