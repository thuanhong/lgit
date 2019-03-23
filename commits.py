import os
from utility import *
from datetime import datetime


def commits(message):
    """
    commits all file have been added in index
    @param message : commit message
    @return None
    """
    set_path(__file__)
    fatal_error()

    new_file = datetime.now().strftime("%Y%m%d%H%M%S.%s")
    file_commits = '.lgit/commits/{}'.format(new_file)
    file_snap = '.lgit/snapshots/{}'.format(new_file)

    content = os.environ['LOGNAME'] + '\n'
    content += datetime.now().strftime("%Y%m%d%H%M%S") + '\n'
    content += '\n' + message + '\n'
    write_file(file_commits, content, 'w')

    file_index = open('.lgit/index', 'r')
    file_snapshots = open(file_snap, 'w')

    write_line = os.open('.lgit/index', os.O_RDWR)
    pos = 0
    os.lseek(write_line, 0, 0)
    for pos_pointer, line in enumerate(file_index.readlines()):
        list_index = line.split()

        sha1_work = get_sha1(list_index[-1])
        str_time = datetime.now().strftime("%Y%m%d%H%M%S")
        content = "{} {} {} {}".format(str_time, sha1_work, list_index[2], list_index[2])
        os.write(write_line, content.encode())
        pos += len(line)
        os.lseek(write_line, pos, 0)

        file_snapshots.write(" ".join(list_index[-2:]) + '\n')
    
    os.close(write_line)
    file_index.close()
    file_snapshots.close()
