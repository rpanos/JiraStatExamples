
import shlex
from subprocess import Popen, PIPE

from sammy_logs.logs_general import Logs_list


def call_cmd(cmd_str):

    args = shlex.split(cmd_str)
    proc = Popen(args, stdout=PIPE)
    output = proc.communicate()[0]

    return output


def does_file_dir_exist(full_file_name, verbose_level=2):
    """
    returns True if file exists, False otherwise
    :param full_file_name: name of directory
    :param verbose_level: if you want info
    """
    ls_cmd = "ls " + full_file_name
    if verbose_level > 4:
        print "\n >> Calling :" + ls_cmd
    output = call_cmd(ls_cmd)
    if verbose_level > 4:
        print ">>" + output
        print ">>len:" + str(len(output))

    # if output is not None and output.find("No such file or directory") > 0:
    if len(output) == 0:
        return False
    else:
        return True


def check_and_set_dir(dir_name, verbose_level=2):
    """
    As long as the directory doesnt already exist, it is created
    :param dir_name: name of directory
    :param verbose_level: if you want info
    :return: void
    """

    base_dir = call_cmd("pwd")

    if not does_file_dir_exist(dir_name):

        dir_name_ls = dir_name.split("/")

        if len(dir_name_ls[-1]) == 0:
            if verbose_level > 4:
                print " >> Removing last blank sub-ish directory "
            dir_name_ls = dir_name_ls[:-1]

        sub_dir = "/".join(dir_name_ls[:-1])  # the last /
        if verbose_level > 4:
            print " \n ########### sub_dir :" + sub_dir

        if base_dir != sub_dir:
            check_and_set_dir(sub_dir)
        elif verbose_level > 4:
            print " \n ########### sub dir is BASE dir " + base_dir

        mkdir_cmd = "mkdir " + dir_name
        output = call_cmd(mkdir_cmd)

        if verbose_level > 4:
            print " ## MKDIR GOT: " + output + "|" + str(len(output)) + "| from :" + mkdir_cmd
        Logs_list.MINING_LOGS.log_lvl_3(" ## MKDIR GOT: " + output + "|"
                                        + str(len(output)) + "| from :" + mkdir_cmd)

    elif verbose_level > 2:
        print " >> DIR already there!"
        Logs_list.MINING_LOGS.log_lvl_3(" >> DIR already there!")

    return




def move_to_file(d_frame, file_dir=None, file_name=None):
    """
    Just a  wrapper function for pandas to_csv

    :param d_frame: dataFrame to be written
    :param file_dir: directory to be written
    :param file_name: filename
    :return: void
    """
    if file_name is None:
        file_name = 'big_matrix.csv'

    if file_dir is None:
        file_dir = 'exported_data/delay_studies/'

    check_and_set_dir(file_dir)

    file_full_path = file_dir + file_name

    d_frame.to_csv(file_full_path, encoding='utf-8')
