"""
file used for print files added but not commit
or untraked file or file have changed but not add
"""
import os
from utility import *


def get_list_status():
    """
    find and store all add, untracked or new files
    @param None
    @return to_be_commit : list files have added but don't commits
    @return not_staged : list files have changed and don't add again
    @return list_tracked : list files have been added in file index
    """
    to_be_commit = []
    not_staged = []
    list_tracked = []
    with open('.lgit/index', 'r') as file_index:
        content = file_index.readlines()
    pos = 0
    for line in content:
        list_line = line.split()
        str_time = get_timestamp(list_line[-1])
        code_sha1 = get_sha1(list_line[-1])
        # append file
        if list_line[2] != list_line[3]:
            to_be_commit.append(list_line[-1])
        if code_sha1 != list_line[1]:
            not_staged.append(list_line[-1])
        # update SHA1 of file working
        content = "{} {}".format(str_time, code_sha1)
        change_hash(pos, content)
        pos += len(line)
        list_tracked.append(list_line[-1])
    return to_be_commit, not_staged, list_tracked


def print_to_be_commit(list_file):
    """
    print all files have added but don't commits
    """
    if list_file:
        print('Changes to be committed:')
        print('  (use "./lgit.py reset HEAD ..." to unstage)\n')
        for element in sorted(list_file, key=len):
            print("     modified: {}".format(element))
        print()


def print_not_staged(list_file):
    """
    print files have changed and don't add again
    """
    if list_file:
        print("\nChanges not staged for commit:")
        print('  (use "./lgit.py add ..." to update what will be committed)')
        print('  (use "./lgit.py checkout -- ..." to discard changes in working directory)\n')
        for element in sorted(list_file, key=len):
            print("     modified: {}".format(element))


def untracked(list_file):
    """
    print files haven't added in file index
    """
    if list_file:
        print("Untracked files:")
        print('  (use "./lgit.py add <file>..." to include in what will be committed)\n')
        for element in sorted(list_file, key=len):
            print("     {}".format(element))
        print('\nnothing added to commit but untracked files present (use "./lgit.py add" to track)')


def get_file_untracked(list_tracked):
    """
    collection all files haven't tracked in file index
    """
    list_file = []
    list_all = []
    for file in os.listdir():
        if not (file.endswith(".py") or file == '.git' or file == '.lgit'):
            list_file.append(file)
    get_path_recursive(list_all, list_file)
    list_file.clear()
    for file in list_all:
        if file not in list_tracked:
            list_file.append(file)
    return list_file


def status():
    """
    handle status
    """
    set_path(__file__)
    fatal_error()
    print("On branch master\n")
    if not os.listdir(".lgit/commits"):
        print("No commits yet\n")

    to_be_commit, not_staged, list_tracked = get_list_status()
    print_to_be_commit(to_be_commit)
    print_not_staged(not_staged)
    untracked(get_file_untracked(list_tracked))
