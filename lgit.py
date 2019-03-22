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


def add_recursive(list_add ,dir=''):
    '''
    handle recursive when add directory and more
    @param list_add : all file need add
    @return None
    '''
    for element in list_add:
        if os.path.isdir(dir + element):
            add_recursive(os.listdir(dir + element), dir + element + '/')
        else:
            add(dir + element)


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
        add_recursive(args.file)
    elif args.command == 'status':
        pass
    elif args.command == 'commit':
        commits(args.m)
    elif args.command == 'log':
        log()
    elif args.command == 'rm':
        rm(args.file[0])