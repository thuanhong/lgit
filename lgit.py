#!/usr/bin/env python3
import os
from hashlib import sha1
from datetime import datetime
from argparse import ArgumentParser
from add import add
from commits import commits
from log import log
from remove import rm
from utility import *
from ls_file import ls_file


def create_lgit():
    """
    create folder .lgit if it not exist
    In folder lgit will have 3 directory and 2 file
    @param None
    @return None
    """
    os.makedirs('.lgit', exist_ok=True)
    os.makedirs('.lgit/commits', exist_ok=True)
    os.makedirs('.lgit/object', exist_ok=True)
    os.makedirs('.lgit/snapshots', exist_ok=True)
    write_file('.lgit/config', os.environ['LOGNAME'], 'w')
    write_file('.lgit/index', '', 'w')


def init():
    """
    handle command init
    """
    if os.path.exists('.lgit'):
        if os.path.isfile('.lgit'):
            os.unlink('.lgit')
            create_lgit()
    else:
        create_lgit()


def handle_add():
    list_path = []
    get_path_recursive(list_path, args.file)
    set_path(__file__)
    for x in list_path:
        add(x)


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
        init()
    elif args.command == 'add':
        handle_add()
    elif args.command == 'status':
        pass
    elif args.command == 'commit':
        commits(args.m)
    elif args.command == 'log':
        log()
    elif args.command == 'rm':
        rm(args.file[0])
    elif args.command == 'ls-file':
        ls_file()