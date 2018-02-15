# -*- coding: utf-8 -*-

def perdelta(start, end, delta):
    """
    :param start: date, datetime
    :param end: date,datetime
    :param delta: timedelta step size
    :return: generator over the dates/datetimes
    """
    curr = start
    while curr <= end:
        yield curr
        curr += delta

def camel_case_to_snake_case(string):
    """
    Converts CamelCase string into snake_case string
    :param string:
    :return:
    """
    step1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', string)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', step1).lower()

def does_file_exist(file_path):
    """
    Boolean, does the file which path is given exist or not
    :param file_path: path of the file which existence is being tested
    :return: True or False
    """
    return os.path.isfile(file_path)


def make_sure_path_exists(path):
    """
    checks whether a directory exists,if not then it tries to create it
    :param path: directory path
    :return: none
    """
    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise


def remove_file(path):
    """
    removes files if it exists
    :param path: path to the file to be removed
    :return:
    """
    try:
        os.remove(path)
    except OSError:
        pass


def remove_folder(path):
    """
    removes folder and its internal elements
    :param path: path to the folder to be removed
    :return:
    """
    try:
        shutil.rmtree(path)
    except OSError:
        sys.exit('ERROR: {0}  could not be removed'.format(path))


def gzip_file(filepath, outfilepath):
    """
    compresses already existing file
    :param filepath: path to file to be compressed
    :param outfilepath: filepath to the compressed file
    :return: none
    """
    with open(filepath, 'rb') as f_in, gzip.open(outfilepath, 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)


def read_file(filepath):
    """
    reads a text file and returns the text as a string
    :param filepath: path to the file
    :return: text
    """
    try:
        with open(filepath, 'r') as myfile:
                text = myfile.read().replace('\n', ' ')
    except IOError:
        sys.exit('{0} Could not be read, check filepath'.format(filepath))

    return text
