#!/usr/bin/env python3
# ------------------------------------------------------------------------------------
# September 2020
#   danianescobarv@gmail.com
# python3.6 script to try functions in function.py:
# 1) def working_path (path)
# 2) def cd_path (working_dir)
# 3) def all_elements(file_xyz)
# 4) def sort_input_pairs(elements)
# ------------------------------------------------------------------------------------

import unittest
import functions as fn
import os
import numpy as np

def drv_cdpath(path):
    """[summary]
    Driver the function cd_path into functions.py
    Args:
        path (string): path of working directory

    Returns:
        working_dir [string]: path of working directory
    """
    fn.cd_path(path)
    working_dir = os.getcwd()
    print("\nfunction cd_path into: ")
    print("cd ",working_dir)
    return working_dir

class Test(unittest.TestCase):
    def test_funtions1(self):
        """[summary]
        Tests of black box to functions into functions.py,
        which use commands of shell: working_path and cd_path
        """

        path = []
        path.append(os.getcwd())
        path.append(os.getcwd())
        self.assertEqual(fn.working_path(path), path[1], "Should be path[0]==path[1]")
        print("\n...Ok  test: working_path")

        self.assertEqual(drv_cdpath(path[0]),path[0], "Should be path[0]")
        print("\n...Ok  test: cdpath")

    def test_functions2(self):
        """[summary]
        Test of black box to functions into functions.py,
        which get atomic pairs
        """

        f = open("1test1.xyz","w")
        f.write('6 \n')
        f.write(' \n')
        f.write('H  0.000 0.000 0.000\n')
        f.write('O  1.000 0.000 0.200\n')
        f.write('Hg 1.000 3.000 0.200\n')
        f.write('C  2.000 0.500 0.200\n')
        f.write('N  1.500 3.300 0.200\n')
        f.write('F  3.500 0.000 0.200')
        f.close()

        pairs_elements = ["H-H", "H-O", "H-Hg", "H-C", "H-N", "H-F", "O-O", "O-Hg",
        "O-C", "O-N", "O-F", "Hg-Hg", "Hg-C", "Hg-N", "Hg-F", "C-C", "C-N", "C-F",
        "N-N", "N-F", "F-F"]
        self.assertEqual(fn.all_elements("1test1.xyz"),pairs_elements)
        print("\n...Ok  test: all_elements")
        os.remove("1test1.xyz")

        pairs_elements1 = ["H-H", "H-O", "O-H", "O-Hg", "Hg-Hg", "Hg-Hg", "Hg-O",
        "F-C", "H-O"]
        pairs_elements2 = ["H-H", "H-O", "O-Hg", "Hg-Hg", "F-C"]
        self.assertEqual(fn.sort_input_pairs(pairs_elements1),pairs_elements2)
        print("\n...Ok  test: sort_input_pairs")

if __name__ == '__main__':
    unittest.main()
    print("\n Everything passed")