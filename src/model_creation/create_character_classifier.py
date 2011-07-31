'''
Created on Jul 19, 2011

@author: kjell
'''
import sys
sys.path.append("../gui")
sys.path.append("../api")
sys.path.append("..")

from java.io import File
from api.simple_image_feature_extractor import SimpleImageFeatureExtractor
from api.character_classifier import CharacterClassifier
from api.specialized_hmm import SpecializedHMM

def create_character_classifier(save_to_file_path):
    example_dir = File("../../character_examples").getPath()
    nr_of_training_examples = 100
    nr_of_test_examples = 0
    
    extractor = SimpleImageFeatureExtractor(nr_of_divisions=11, 
                                            size_classification_factor=4.6)
    
    training_examples, test_examples = extractor.extract_training_and_test_examples(example_dir, 
                                                                                   nr_of_training_examples, 
                                                                                   nr_of_test_examples)
    classifier = CharacterClassifier(training_examples,
                                     nr_of_hmms_to_try=1,
                                     fraction_of_examples_for_test=0,
                                     train_with_examples=False,
                                     initialisation_method=SpecializedHMM.InitMethod.count_based,
                                     feature_extractor=extractor)
    #test_result = str(classifier.test(test_examples))
    #print(test_result)
    classifier_string = classifier.to_string()
    file = open(save_to_file_path + ".dat",'w')
    file.write(classifier_string)
    file.close()

if __name__ == '__main__':
    create_character_classifier("character_classifier_11_segments_4_6_cf")