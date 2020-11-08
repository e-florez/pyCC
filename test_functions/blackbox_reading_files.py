import unittest
import functions as fn
import function_files as fn1

class Test(unittest.TestCase):
    def test_funtions1(self):
        """
        Función que verifica la función reading_files_XYZ en functions,
        creado por Cesar, la cual devuelve una lista, list_xyz, con los
        nombre de los archivos .xyz en orden
        """
        list_files = ['aw1s1.xyz', 'bw1s1.xyz']
        self.assertEqual(fn.reading_files_XYZ(), list_files, "Should be list_xyz==list_files")
        print("\n...Ok  test: functions.reading_files_XYZ")
    def test_funtions2(self):
        """
        Función que verifica la función reading_files en function_files.py,
        creado por Cesar, la cual devuelve una lista, list_xyz, con los
        nombre de los archivos .xyz en orden
        """

        list_files = ['aw1s1.xyz', 'bw1s1.xyz']
        repited_list_xyz = []  # repited files (if any)
        list_xyz = []  # unique files
        self.assertEqual(fn1.reading_files(list_xyz,repited_list_xyz), list_files, "Should be list_xyz==list_files")
        print("\n...Ok  test: funtion_files.reading_files")
if __name__ == '__main__':
    unittest.main()
    print("\n Everything passed")