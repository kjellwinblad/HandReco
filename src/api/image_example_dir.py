'''
Created on Jul 9, 2011

@author: kjell
'''

import unittest
import os
import java
from java.io import File, FileOutputStream, FileInputStream
from javax.imageio import ImageIO
import inspect


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
    
    def save_example(self, label, image_byte_array):
        output_file_name = label + "_" + str(java.lang.System.currentTimeMillis()) + ".png"
        save_path = File(self.dir_path, output_file_name).getCanonicalPath()
        fileos = FileOutputStream(save_path)
        for byte in image_byte_array:
            fileos.write(byte)
        fileos.flush()
        fileos.close()
    
    def __iter__(self):
        dir_path = self.dir_path
        class ImageExampleDirIter:
            
            def next(self):
                image_file_name = self.iterator.next()
                #Find example label
                label = image_file_name[0:image_file_name.index('_')]
                #Get the image as an image buffer
                image_file = File(dir_path, image_file_name)
                image_is = FileInputStream(image_file)
                buffered_image = ImageIO.read(image_is)
                #Return label and image tuple
                return (label, buffered_image)
            
            def __init__(self, iter_list):
                self.iterator = iter_list.__iter__()
        
        self.reload_elements()
        return ImageExampleDirIter(self.example_list)
        
    
class TestImageExampleDir(unittest.TestCase):
    
    def test_image_example_dir_iteration(self):
        f = File(str(inspect.getfile( inspect.currentframe() )))
        example_dir = File(File(f.getParentFile().getParentFile().getParentFile(),"character_examples"),"A")
        image_example_dir = ImageExampleDir(example_dir.getCanonicalPath())
        for label, image in image_example_dir:
            if label != "A":
                raise "The label of the examples in this dir should be A"

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()
