'''
Created on Jul 18, 2011

@author: kjell
'''
from api.image_preprocessor import scale_to_fill, divide_into_segments,\
    extract_sorted_component_size_list
import unittest
from java.io import File
import inspect
from api.image_example_dir import ImageExampleDir
import os

class SimpleImageFeatureExtractor(object):
    '''
    A class used to extract a sequence of features from an image that
    may be used as training observations for a HMM.
    '''
    
    feature_pattern_to_id = {"LLL":"a",
                             "LLS":"b",
                             "LSS":"c",
                             "LSN":"d",
                             "LLN":"e",
                             "LNN":"f",
                             "SSS":"g",
                             "SSN":"h",
                             "SNN":"i",
                             "NNN":"j"}

    def __init__(self,
                 nr_of_divisions=7, 
                 size_classification_factor=1.3):
        '''
        Parameters:
        * nr_of_divisions - Number of times to divide the image vertically
        * size_classification_factor -  A component in a segment is classified
        as small if the component size is less than "segment_width * size_classification_factor"
        and greater than zero otherwise it is classified as large. Zero size segments are 
        classified as none.
        * nr_of_components_to_consider - The number of components to consider
        
        The 3 largest components in a segment are used to get a feature for that segment. 
        There are 10 different possible features in every segment. The features are enumerated 
        in the following list:
        
        feature id | comp. 1 | comp. 2 | comp. 3
        a          | L       | L       | L       |
        b          | L       | L       | S       |
        c          | L       | S       | S       |
        d          | L       | S       | N       |
        e          | L       | L       | N       |
        f          | L       | N       | N       |
        g          | S       | S       | S       |
        h          | S       | S       | N       |
        i          | S       | N       | N       |
        j          | N       | N       | N       |
        
        comp. = component
        L = large
        S = small
        N = none
        '''
        self.nr_of_divisions = nr_of_divisions
        self.size_classification_factor = size_classification_factor
      
    def extract_feature_string(self,buffered_image):
        scaled_image = scale_to_fill(buffered_image)
        segments = divide_into_segments(self.nr_of_divisions, scaled_image)
        #Get component sizes for the segments
        features_for_segments = [extract_sorted_component_size_list(s)
                                 for s in segments]
        #Make sure that there are 3 elements on the list for all segmensts
        def make_size_of_list3(list):
            if len(list)==3:
                return list
            elif len(list)>3:
                del list[len(list)-1]
                return make_size_of_list3(list)
            elif len(list)<3:
                list.append(0)
                return make_size_of_list3(list)
        features_for_segments = [make_size_of_list3(l)
                                 for l in features_for_segments]
        def classify_component(component_size, segment_width):
            if component_size >= (segment_width * self.size_classification_factor):
                return "L"
            elif component_size != 0:
                return "S"
            else:
                return "N"
        feature_string = ""
        for i in range(self.nr_of_divisions):
            segment_comp_sizes = features_for_segments[i]
            segment = segments[i]
            segment_width = segment.getWidth()
            segment_feature_string = ""
            for size in segment_comp_sizes:
                segment_feature_string = (segment_feature_string + 
                                          classify_component(size, segment_width))
            feature_string = (feature_string + 
                              self.feature_pattern_to_id[segment_feature_string])
        return feature_string
    
    def extract_feature_strings_for_dir(self,dir_path):
        image_dir = ImageExampleDir(dir_path)
        images = [image for (label,image) in image_dir]
        feature_strings = [self.extract_feature_string(image) for image in images]
        return feature_strings
    
    def extract_label_examples_tuples_for_library(self,library_path):
        example_dirs =  os.listdir(library_path)
        label_example_tuples = []
        for dir_name in example_dirs:
            label = dir_name
            dir = File(File(library_path), dir_name).getCanonicalPath()
            examples = self.extract_feature_strings_for_dir(dir)
            label_example_tuples.append((label, examples))
        return label_example_tuples
                
class TestSimpleImageFeatureExtractor(unittest.TestCase):
    
    def get_example_image(self):
        f = File(str(inspect.getfile( inspect.currentframe() )))
        example_dir = File(File(f.getParentFile().getParentFile().getParentFile(),"character_examples"),"A")
        image_example_dir = ImageExampleDir(example_dir.getCanonicalPath())
        label, image = image_example_dir.__iter__().next()
        return image
    
    def test_extract_feature_string(self):
        image = self.get_example_image()
        extractor = SimpleImageFeatureExtractor(nr_of_divisions=7, 
                                                size_classification_factor=1.3)
        feature_string = extractor.extract_feature_string(image)
        print("test_extract_feature_string")
        print(feature_string)
        
    def test_extract_feature_strings_for_dir(self):
        extractor = SimpleImageFeatureExtractor(nr_of_divisions=7, 
                                                size_classification_factor=1.3)
        f = File(str(inspect.getfile( inspect.currentframe() )))
        example_dir_path = File(File(f.getParentFile().getParentFile().getParentFile(),
                                     "character_examples"),
                                "A").getCanonicalPath()
        feature_strings = extractor.extract_feature_strings_for_dir(example_dir_path)
        print("test_extract_feature_strings_for_dir")
        print(feature_strings)
        
    def test_extract_label_examples_tuples_for_library(self):
        extractor = SimpleImageFeatureExtractor(nr_of_divisions=7, 
                                                size_classification_factor=1.3)
        f = File(str(inspect.getfile( inspect.currentframe() )))
        library_path = File(f.getParentFile().getParentFile().getParentFile(),
                                     "character_examples").getCanonicalPath()
        training_examples = extractor.extract_label_examples_tuples_for_library(library_path)
        print("test_extract_label_examples_tuples_for_library")
        print(training_examples)
        


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main() 
            
            
            
        
    
        