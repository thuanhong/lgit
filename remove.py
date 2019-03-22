from os import unlink
from utility import check_file, get_path


def rm(file_name):
    if check_file(file_name):
        return
    file_name = get_path(file_name)
    file = open('.lgit/index', 'r')
    output = []
    for line in file:
        if not line.endswith(file_name + '\n'):
            output.append(line)
    file.close()
    file = open('.lgit/index', 'w')
    file.writelines(output)
    file.close()
    unlink(file_name)