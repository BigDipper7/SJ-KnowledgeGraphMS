import os, datetime
import logging

def create_file_with_time(root_path, file_name):
    if not root_path or not file_name:
        raise Exception('root_path or file_name can not be empty! check it!')

    final_dir=''
    try:
        final_dir = _create_dir_with_time(root_path)
    except Exception as e:
        raise

    final_dir = os.path.join(final_dir, file_name)

    logging.info("[file_util]: success get file dir: \n' {} '".format(final_dir))

    return final_dir

def _create_dir_with_time(root_path):
    '''create a dir with specified root_path and timestamp
        return the success create dir
    '''
    if not root_path:
        raise Exception("root_path can not be empty!!")

    final_dir = os.path.join(root_path, datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))

    try:
        os.makedirs(final_dir)
    except OSError, e:
        if e.errno != 17:
            raise # This was not a "directory exist" error..
    # with open(os.path.join(mydir, filename), 'w') as d:
    #     d.writelines(list)

    logging.info("[file_util]: success get folder dir with timestamp: \n' {} '".format(final_dir))

    return final_dir
