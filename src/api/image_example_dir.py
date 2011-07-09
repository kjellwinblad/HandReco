'''
Created on Jul 9, 2011

@author: kjell
'''

import unittest
import os
import java
from java.io import File, FileOutputStream

class ImageExampleDir:
    '''
    Handler for a directory containing image examples
    '''

    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.reload_elements()
    
    def reload_elements(self):
        files_in_dir = os.listdir(self.dir_path)
        self.example_list = [elem for elem in files_in_dir if elem.endswith(".png") and ("_" in elem)]
        print(self.example_list)
    
    def save_example(self, label, image_byte_array):
        output_file_name = label + "_" + str(java.lang.System.currentTimeMillis()) + ".png"
        save_path = File(self.dir_path, output_file_name).getCanonicalPath()
        fileos = FileOutputStream(save_path)
        for byte in image_byte_array:
            fileos.write(byte)
        fileos.flush()
        fileos.close()
        
    
class TestImageExampleDir(unittest.TestCase):
    print("no test yet")

        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()