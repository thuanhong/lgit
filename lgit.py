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
from ls_file import ls_files
from status import status


def create_lgit():
    """
    create folder .lgit if it not exist or missing
    In folder lgit will have 3 directory and 2 file
    @param None
    @return None
    """
    os.makedirs('.lgit', exist_ok=True)
    os.makedirs('.lgit/commits', exist_ok=True)
    os.makedirs('.lgit/objects', exist_ok=True)
    os.makedirs('.lgit/snapshots', exist_ok=True)
    write_file('.lgit/config', os.environ['LOGNAME'], 'w')
    write_file('.lgit/index', '', 'w')


def init():
    """
    handle command init

    """
    set_path(__file__)
    if os.path.exists('.lgit'):
        if os.path.isfile('.lgit'):
            os.unlink('.lgit')
            create_lgit()
        else:
            print("Git repository already initialized.")
    else:
        create_lgit()


def handle_add(list_file):
    """
    execute command add
    use recursive to take file in directory if input is directory
    """
    list_path = []
    get_path_recursive(list_path, list_file)
    set_path(__file__)
    for file in list_path:
        add(file)


def take_argument():
    """
    take agument (like : add, init, status, ...)
    @param None
    @return a object contain argument
    """
    parser = ArgumentParser()
    parser.add_argument("command", help="input command need execute")
    parser.add_argument("file", nargs="*", help="add file need handle")
    parser.add_argument("--author", type=str, help="config into account")
    parser.add_argument("-m", type=str, help="commit message")
    return parser.parse_args()


def main():
    """
    handle main
    """
    argument = take_argument()
    if argument.command == 'init':
        init()
    elif argument.command == 'add':
        handle_add(argument.file)
    elif argument.command == 'status':
        status()
    elif argument.command == 'commit':
        commits(argument.m)
    elif argument.command == 'log':
        log()
    elif argument.command == 'rm':
        rm(argument.file[0])
    elif argument.command == 'ls-files':
        ls_files()
    elif argument.command == 'config':
        set_path(__file__)
        write_file('.lgit/config', argument.author + '\n', 'w')



if __name__ == "__main__":
    main()
