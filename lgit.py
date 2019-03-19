#!/usr/bin/env python3
import os
from hashlib import sha1
from argparse import ArgumentParser


def write_file(name_file, content):
    file = open(name_file, 'w')
    file.write(content)
    file.close()


def create_init():
    os.mkdir('.lgit')
    os.mkdir('.lgit/commits')
    os.mkdir('.lgit/object')
    os.mkdir('.lgit/snapshots')
    write_file('.lgit/config', os.environ['LOGNAME'])
    write_file('.lgit/index', '')


def take_argument():
    parser = ArgumentParser()
    parser.add_argument("command", help="input command need execute")
    parser.add_argument("file", nargs="*", help="add file need handle")
    return parser.parse_args()


def handle_init():
    if os.path.exists('.lgit'):
        if os.path.isfile('.lgit'):
            os.unlink('.lgit')
            create_init()
    else:
        create_init()


def fatal_error():
    if not os.path.exists('.lgit'):
        print("Reinitialized existing Git repository in " + os.getcwd())
        return True
    return False


def handle_add(list_file):
    if fatal_error():
        return
    for file in list_file:
        try:
            file = open(file, 'r')
        except:
            print('fatal: pathspec ' + file + ' did not match any files')
            return
        content = file.read()
        code_sha1 = sha1(content.encode()).hexdigest()
        print(content)
        os.makedirs('.lgit/object/' + code_sha1[:2])
        write_file('.lgit/object/' + code_sha1[:2] + '/' + code_sha1[2:], content)


if __name__ == "__main__":
    args = take_argument()
    if args.command == 'init':
        handle_init()
    elif args.command == 'add':
        handle_add(args.file)
