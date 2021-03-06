import json
import logging
from unidecode import unidecode
from os.path import isfile, exists, join, isdir
from os import rename, listdir, mkdir
from datetime import datetime


def write_file(data, file_pathname, mode='w'):
    """
    Creates or overwrite a new file
    :param data: list() of dict()
    :param file_pathname: str
    :return: Creates a JSON file
    """
    if '.json' in file_pathname:
        with open(file_pathname, mode, encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    elif '.txt' in file_pathname:
        with open(file_pathname, mode, encoding='utf-8') as file:
            file.write(data)


def open_file(file_pathname):
    """
    Opens a file
    :param file_pathname: str
    :return: Creates a JSON file
    """
    if '.json' in file_pathname:
        with open(file_pathname, 'r', encoding='utf-8') as file:
            data = json.load(file)

    elif '.txt' in file_pathname:
        with open(file_pathname, 'r') as file:
            data = file.read()

    return data


def rename_file(data, old_path, new_path):
    """
    Renames and moves files
    :param data: list() of dict()
    :param old_path: str
    :param new_path: str
    :param final: bool (optional), if selected it will create a file_pathname using a different format for final storage
    :return: null
    """
    if exists(old_path) and isfile(old_path):
        rename(old_path, new_path)
        write_file(data, new_path)


def remove_duplicates(mylist):
    """
    Remove duplicate entries
    :param mylist: a list() of dict()
    :return: a list() of dict()
    """
    myset = set()
    new_list = []
    for employee in mylist:
        mytuple = tuple(employee.items())
        if mytuple not in myset:
            myset.add(mytuple)
            new_list.append(employee)
    return new_list


def normalize_string(str_):
    return unidecode(str_).lower()


def get_folder_files(pathdir, file_types):
    """
    Get files from a folder
    :param pathdir: directory path of the folder
    :param file_types: a list containing the types of files to be selected
        Example: ['json, txt]'
    :return: a list of pathnames
    """
    file_list = []
    if exists(pathdir) and isdir(pathdir):
        for file in listdir(pathdir):
            file_pathname = join(pathdir, file)
            if isfile(file_pathname):
                for file_type in file_types:
                    if file_type in normalize_string(file_pathname):
                        file_list.append(file_pathname)
    return file_list


def create_path(filename='', folder='', final=False):
    """
    Creates a new file_pathname
    :param final: bool, optional, formats the pathname differently when the whole data extraction is completed
    :return: a string with a new file_pathname
    """
    if final:
        filename = filename.split('_page_')[0] + '.json'

    elif not exists(folder):
        mkdir(folder)

    date = datetime.today().strftime('%Y-%m-%d')
    file_path = join(folder, f'{date}_{filename}')
    return file_path


def start_logger(name):
    logger = logging.getLogger(name)
    logger.level = 20
    logging.basicConfig(
        format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s: %(message)s',
        datefmt='%d/%m/%Y %I:%M:%S %p', level=20)

    return logger

# def update_database(mylist, mydb):
#     fh = open('list.pkl', 'wb')
#     pickle.dump(mydb, fh)
#     fh.close()
#
#     fh = open('list.pkl', 'rb')
#     links = pickle.load(fh)
#     fh.close()
#
#     links.extend(mylist)
#     fh = open('list.pkl', 'wb')
#     pickle.dump(links, fh)
#     fh.close()
