'''
Created on Jul 28, 2011

@author: Lenovo
'''
from api.image_example_dir import ImageExampleDir
from java.io import File

path = File(File(File(File(".."),".."), "word_examples_for_test"),"A").getCanonicalPath()

print(path)
image_example_dir = ImageExampleDir(path)
list_of_images = [image for label,image in image_example_dir]

for image in list_of_images:
    print image