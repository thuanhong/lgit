import os
from utility import *


def add(file_name):
    """
    handle command add
    Store file content with their SHA1 hash value
    the first two characters of the SHA1 will be the directory name
    the last 38 characters will be the file name
    @param list_file : all file need add
    @return output error (if possible)
    """
    if fatal_error() or check_file(file_name):
        return
    file = open(file_name, 'r')
    content = file.read()
    code_sha1 = sha1(content.encode()).hexdigest()
    os.makedirs('.lgit/object/' + code_sha1[:2], exist_ok=True)
    new_file = '.lgit/object/{}/{}'.format(code_sha1[:2], code_sha1[2:])
    write_file(new_file, content, 'w')
    update_index(file_name, code_sha1)


def update_index(file_name, sha1):
    """
    update content of file index
    include timestamps,
            the SHA1 of the content in the working,
            the SHA1 after lgit add it,
            the SHA1 after lgit commit it,
            file pathname
    @param None
    @return None
    """
    # get timestamp of file
    str_time = get_timestamp(file_name)

    # write new value if file is empty
    if os.path.getsize('.lgit/index') == 0:
        content = '{} {} {} {} {}\n'.format(str_time, sha1, sha1, " "*40, file_name)
        write_file('.lgit/index', content, 'a')
        return

    # write value hash SHA1 when execute add or commit
    file = open('.lgit/index', 'r')
    write_line = os.open('.lgit/index', os.O_RDWR)
    pos = 0
    os.lseek(write_line, pos, 0)
    for pos_pointer, line in enumerate(file.readlines()):
        if file_name in line:
            # rewrite only the line have file name
            # replace old SHA1 by new SHA1
            content = "{} {} {}".format(str_time, sha1, sha1)
            os.write(write_line, content.encode())
            os.close(write_line)
            file.close()
            return
        pos += len(line)
        os.lseek(write_line, pos, 0)
    else:
    # append new value to the end file if the file haven't been written
        file.close()
        content = '{} {} {} {} {}\n'.format(str_time, sha1, sha1, " "*40, file_name)
        write_file('.lgit/index', content, 'a')
