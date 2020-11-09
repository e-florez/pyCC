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
#
#   cesar-b29@hotmail.com

# ------------------------------------------------------------------------------------
# Description:

# ------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# ------ Main body
# ------------------------------------------------------------------------------------

def working_directory(arg_prompt):
    import os  # - to check id a file or dir exits -> os.path.exists()

    """[summary]
    Asking or taking path of working directory from argument of prompt and
    verification of working directory

    Args:
        arg_prompt (str): argument in the prompt when was execution of program
    """

    if len(arg_prompt) <= 1 : #argument from prompt shell is not vaccum
        tmp_dir =  input(f'\nAddress of directory (whit the XYZ files) [default: empty]: ')
        tmp_dir = tmp_dir.strip()

        if tmp_dir == '.' or len(tmp_dir) < 1: #get path of current directory
            working_dir = os.getcwd()
        else:  #get full path of working directory
            if tmp_dir[0] == "/":
                working_dir = tmp_dir
            else:
                working_dir =  str(os.getcwd()) + "/" + str(tmp_dir)

    elif arg_prompt[1] == '.' : #argument from prompt shell indicate the current directory
        working_dir = os.getcwd()

    else:   #argument from prompt shell is vaccum
        if arg_prompt[1][0] == "/" :  #Full path (Since the root)
            working_dir = arg_prompt[1]
        else:                         #Path incompleted
            working_dir =  str(os.getcwd()) + "/" + str(arg_prompt[1])

    print(f'\nWorking directiry: {working_dir}')   #Working directory

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
            if read_permission == False:
                print(f"\n Read permission missing")
            if write_permission == False:
                print(f"\n Write permission missing")
            if execution_permission == False:
                print(f"\n Execution permission missing")
            if save_new_file_permission == False:
                print(f"\n Save new files permission missing")
            exit(f'\n*** Directory permissions insufficient ***')
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
