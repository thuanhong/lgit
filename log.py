"""
file used for print commits history (if possible)
"""
from os import listdir, stat
from time import ctime
from utility import set_path


def log():
    """
    print all all those commits you did
    sorted in descending order
    @param None
    @return None
    """
    # get all file commit in folder commits
    set_path(__file__)
    list_file = listdir('.lgit/commits')
    for file_commit in list_file:
        file = open('.lgit/commits/' + file_commit, 'r')
        # Read each line of the file as a list
        list_content = file.readlines()
        file_path = '.lgit/commits/' + file_commit
        # print following information intra
        print_commit(file_commit, list_content, file_path)
        file.close()
        if list_file[-1] != file_commit:
            print('\n')


def print_commit(file_name, content, file_path):
    """
    display all commits with the following information
    @param file_name : file name
    @param content : content of file as a list
    @param file_path : file path
    @return None
    """
    print("commit {}".format(file_name))
    print("Author: {}".format(content[0].rstrip()))
    print("Date: {}\n".format(ctime(stat(file_path).st_ctime)))
    print("	 {}".format(content[3].rstrip('\n')))
