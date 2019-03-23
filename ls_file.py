from utility import set_path


def ls_file():
    set_path(__file__)
    file_index = open('.lgit/index')
    for line in file_index:
        print(line.split()[-1])
    file_index.close()