import os
from utility import *
from datetime import datetime


def commits(message):
    """
    commits all file have been added in index
    @param message : commit message
    @return None
    """
    if fatal_error():
        return
    new_file = datetime.now().strftime("%Y%m%d%H%M%S.%s")
    file_commits = '.lgit/commits/{}'.format(new_file)
    file_snap = '.lgit/snapshots/{}'.format(new_file)

    content = os.environ['LOGNAME'] + '\n'
    content += datetime.now().strftime("%Y%m%d%H%M%S") + '\n'
    content += '\n' + message + '\n'
    write_file(file_commits, content, 'w')

    file_index = open('.lgit/index', 'r')
    file_snapshots = open(file_snap, 'w')
    for pos_pointer, line in enumerate(file_index.readlines()):
        line = line.split()

        sha1_work = get_sha1(line[-1])
        str_time = datetime.now().strftime("%Y%m%d%H%M%S")
        content = "{} {} {} {}".format(str_time, sha1_work, line[2], line[2])

        write_line = os.open('.lgit/index', os.O_RDWR)
        os.lseek(write_line, pos_pointer*143, 0)
        os.write(write_line, content.encode())
        os.close(write_line)

        file_snapshots.write(" ".join(line[-2:]) + '\n')

    file_index.close()
    file_snapshots.close()
