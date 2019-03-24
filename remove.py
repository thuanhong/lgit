"""
file used for remove a file
print error if file not exist or file not add yet
"""
from os import unlink
from utility import check_file, get_path, set_path


def rm(file_name):
    """
    remove a file
    change content of index (if need) by remove old file and create new file
    @param file_name : file name
    @return None
    """
    # Check if the file exists
    check_file(file_name)
    # get file path from the directory contain .lgit to file
    file_name = get_path(file_name)
    # change directory working
    set_path(__file__)
    # check if the file in file index
    check_tracked(file_name)
    # take content all file don't need remove
    file = open('.lgit/index', 'r')
    output = []
    for line in file:
        if line.split()[-1] != file_name:
            output.append(line)
    file.close()
    # Write the content to a new file index
    file = open('.lgit/index', 'w')
    file.writelines(output)
    file.close()
    unlink(file_name)


def check_tracked(file_name):
    """
    check if the file in file index
    @param file_name : file name
    @return None
    """
    file = open('.lgit/index')
    for line in file:
        if line.split()[-1] == file_name:
            return
    print("fatal: pathspec '" + file_name + "' did not match any files")
    quit()
