import subprocess

from aiogram.filters import and_f


def process_exists(process_name):
    processes = str(subprocess.check_output('tasklist'))
    if process_name in processes:
        return True
    else:
        return False

def processes_exist(process_list):
    second_condition: bool = True
    processes = str(subprocess.check_output('tasklist'))
    for process in process_list:
        if process in processes:
            first_condition = True
        else:
            first_condition = False
        second_condition = first_condition and second_condition
    return second_condition
