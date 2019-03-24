"""
file used for handle command lgit.py commit -m <message>
change content of file index
change the name of the author in lgit/config (if possible)
"""
import os
from utility import *
from datetime import datetime


def check_config():
    """
    quit program if file config empty
    """
    if not os.path.getsize(".lgit/config"):
        quit()


def commits(message):
    """
    commits all file have been added in index
    change the name of the author
    change content of index file
    @param message : commit message
    @return None
    """
    set_path(__file__) # change directory working become the path script
    fatal_error() # check folder init (quit if the init not exist)
    check_config() # check author (quit if the config haven't author)
    # get time when execute commit (now)
    new_file = datetime.now().strftime("%Y%m%d%H%M%S.%s")
    write_file_commit(new_file, message)
    write_snapshot_index(new_file)


def write_file_commit(new_file, message):
    """
    create new file in foler commits and write content into file
    @param new_file : name of new file base on time now
    @return None
    """
    file_commits = '.lgit/commits/{}'.format(new_file)
    # write content into file commits just created
    content = os.environ['LOGNAME'] + '\n'
    content += datetime.now().strftime("%Y%m%d%H%M%S") + '\n'
    content += '\n' + message + '\n'
    write_file(file_commits, content, 'w')


def write_snapshot_index(new_file):
    """
    open file snapshots just created and file index to write content
    @param new_file : name of new file base on time now
    @return None
    """
    file_snap = '.lgit/snapshots/{}'.format(new_file)
    file_snapshots = open(file_snap, 'w')
    # open file to read content
    file_index = open('.lgit/index', 'r')
    # set position first
    pos = 0
    for pos_pointer, line in enumerate(file_index.readlines()):
        list_index = line.split()
        # get content from SHA1, time, ...
        sha1_work = get_sha1(list_index[-1])
        str_time = datetime.now().strftime("%Y%m%d%H%M%S")
        content = "{} {} {} {}".format(str_time, sha1_work,
                                       list_index[2], list_index[2])
        change_hash(pos, content)
        # set a new position
        pos += len(line)
        # write content into file snapshots include : SHA1 hash and file path
        file_snapshots.write(" ".join(list_index[-2:]) + '\n')
    file_index.close()
    file_snapshots.close()
