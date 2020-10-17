#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# July 2020
#
# python3.x script by:
#
#   name        : Edison Florez (github.com/e-florez/)
#   email       : edisonffh@gmail.com
#   affiliation : Massey University, New Zealand
#
#   name        : Andy Zapata (github.com/AndyDanian)
#   email       : danianescobarv@gmail.com
#   affiliation : Institute of Modelling and Innovative Technology (CONICET-IMIT), Argentina
#
#   cesar-b29@hotmail.com

# ------------------------------------------------------------------------------------
# Description:

# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

import os  # - to check id a file or dir exits -> os.path.exists()

def working_directory(arg_prompt):
    """[summary]
    Asking or taking path of working directory from argument of prompt and
    verification of working directory

    Args:
        arg_prompt (str): argument in the prompt when was execution of program
    """

    if len(arg_prompt) <= 1 :
        tmp_dir =  input(f'\nAddress of directory (whit the XYZ files) [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        if tmp_dir == '.' or  '..' in tmp_dir or len(tmp_dir) < 1:
            if tmp_dir == '.' or len(tmp_dir) < 1 :
                working_dir = os.getcwd()
            elif '../..' in tmp_dir:
                print(f'\n*** ERROR ***')
                exit(f'Only accept one return')
            else:
                ndirectories = len(os.getcwd().split("/"))
                len_name_directory = len(os.getcwd().split("/")[ndirectories-1]) + 1
                len_address = len(os.getcwd()) - len_name_directory
                working_dir = os.getcwd().strip()[0:len_address]
        else:
            first_directory = os.getcwd().split("/")[1]
            if first_directory in tmp_dir :
                working_dir = tmp_dir
            else:
                print(f'\n*** ERROR ***')
                print(f'Address incomplete')
                exit(f'Put on all the explicit address')

    elif arg_prompt[1] == '.' or '..' in arg_prompt[1] :
        if arg_prompt[1] == '.' :
            working_dir = os.getcwd()
        elif '../..' in arg_prompt[1] :
            print(f'\n*** ERROR ***')
            exit(f'Only accept one return')
        else:
            ndirectories = len(os.getcwd().split("/"))
            len_name_directory = len(os.getcwd().split("/")[ndirectories-1]) + 1
            len_address = len(os.getcwd()) - len_name_directory
            working_dir = os.getcwd().strip()[0:len_address]
    else:
        working_dir = arg_prompt[1]

    print(f'\nWorking directiry: {working_dir}')

    # Check if the working dir exists
    if os.path.exists(working_dir) :
        #Verification of permission of directory
        read_permission = os.access(working_dir, os.R_OK)
        write_permission = os.access(working_dir, os.W_OK)
        execution_permission = os.access(working_dir, os.X_OK)
        save_new_file_permission = os.access(working_dir, os.X_OK | os.W_OK)
        if read_permission == True and write_permission == True and\
            execution_permission == True and save_new_file_permission == True:
            # Change the current working Directory
            os.chdir(working_dir)
        else:
            print(f'\n*** ERROR ***')
            exit(f'Directory permissions insufficient')
    else:
        print(f'\n*** ERROR ***')
        exit(f"Can't change the Working Directory, {working_dir} doesn't exist")

def reading_files_XYZ():
    """
       [summary]

       input: a, b, c
       output: d

       Args:
           a (str): distancia
           b ([type]): [description]
           c ([type]): [description]
           d ([type]): [description]
    """
    pass


def format_files_XYZ():
    """
       [summary]

       input: a, b, c
       output: d

       Args:
           a (str): distancia
           b ([type]): [description]
           c ([type]): [description]
           d ([type]): [description]
    """
    pass
