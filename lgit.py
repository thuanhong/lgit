#!/usr/bin/env python3
import os
from hashlib import sha1
from datetime import datetime
from argparse import ArgumentParser


def write_file(name_file, content, mode):
    """
    write content into file
    @param name_file : file name
    @param content : Content will be written to the file
    @param mode : methods (modes) for opening a file
    @return None
    """
    file = open(name_file, mode)
    file.write(content)
    file.close()


def create_lgit():
    """
    create folder .lgit if it not exist
    In folder lgit will have 3 directory and 2 file
    @param None
    @return None
    """
    os.mkdir('.lgit')
    os.mkdir('.lgit/commits')
    os.mkdir('.lgit/object')
    os.mkdir('.lgit/snapshots')
    write_file('.lgit/config', os.environ['LOGNAME'], 'w')
    write_file('.lgit/index', '', 'w')


def handle_init():
    """
    handle command init
    """
    if os.path.exists('.lgit'):
        if os.path.isfile('.lgit'):
            os.unlink('.lgit')
            create_lgit()
    else:
        create_lgit()


def fatal_error():
    """
    catch error if the program execute commands as : add, status, ...
    without folder init
    @param None
    @return True if lgit have a fatal error, otherwise return False
    """
    if not os.path.exists('.lgit'):
        print("Reinitialized existing Git repository in " + os.getcwd())
        return True
    return False


def handle_add(list_file):
    """
    handle command add
    Store file content with their SHA1 hash value
    the first two characters of the SHA1 will be the directory name
    the last 38 characters will be the file name
    @param list_file : all file need add
    @return output error (if possible)
    """
    if fatal_error():
        return
    for file_name in list_file:
        try:
            file = open(file_name, 'r')
        except:
            print('fatal: pathspec ' + file + ' did not match any files')
            return
        content = file.read()
        code_sha1 = sha1(content.encode()).hexdigest()
        os.makedirs('.lgit/object/' + code_sha1[:2], exist_ok=True)
        new_file = '.lgit/object/{}/{}'.format(code_sha1[:2], code_sha1[2:])
        write_file(new_file, content, 'w')
        update_index(file_name, code_sha1)


def get_timestamp(file_name):
    """
    get last modify time of file or directory
    @param file_name : name of file or directory
    @return timestamps of file
    """
    mod_time = os.stat(file_name).st_mtime
    return datetime.fromtimestamp(mod_time).strftime("%Y%m%d%H%M%S")


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
    for pos_pointer, line in enumerate(file.readlines()):
        if file_name in line:
            # rewrite only the line have file name
            # replace old SHA1 by new SHA1
            write_line = os.open('.lgit/index', os.O_RDWR)
            os.lseek(write_line, pos_pointer*143, 0)
            content = "{} {} {}".format(str_time, sha1, sha1)
            os.write(write_line, content.encode())
            os.close(write_line)
            file.close()
            return
    else:
    # append new value to the end file if the file haven't been written
        file.close()
        content = '{} {} {} {} {}\n'.format(str_time, sha1, sha1, " "*40, file_name)
        write_file('.lgit/index', content, 'a')


def get_sha1(file_name):
    file = open(file_name, 'r')
    code_sha1 = sha1(file.read().encode()).hexdigest()
    file.close()
    return code_sha1


def handle_commit(message):
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

        write_line = os.open('.lgit/index', os.O_RDWR)
        os.lseek(write_line, pos_pointer*143, 0)

        content = "{} {} {} {}".format(str_time, sha1_work, line[2], line[2])
        os.write(write_line, content.encode())
        os.close(write_line)

        file_snapshots.write(" ".join(line[-2:]) + '\n')


    file_index.close()
    file_snapshots.close()


def take_argument():
    """
    take agument (like : add, init, status, ...)
    @param None
    @return a object contain argument
    """
    parser = ArgumentParser()
    parser.add_argument("command", help="input command need execute")
    parser.add_argument("file", nargs="*", help="add file need handle")
    parser.add_argument("-m", type=str, help="commit message")
    return parser.parse_args()


if __name__ == "__main__":
    args = take_argument()
    if args.command == 'init':
        handle_init()
    elif args.command == 'add':
        handle_add(args.file)
    elif args.command == 'status':
        pass
    elif args.command == 'commit':
        handle_commit(args.m)
