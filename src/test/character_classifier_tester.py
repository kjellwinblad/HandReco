'''
Created on Jul 19, 2011

@author: kjell
'''
import sys
sys.path.append("../gui")
sys.path.append("../api")
sys.path.append("..")
from api.simple_image_feature_extractor import SimpleImageFeatureExtractor
from api.character_classifier import CharacterClassifier

from api.word_examples_generator import generate_examples_for_words
from api.word_classifier import WordClassifier
from api.specialized_hmm import SpecializedHMM
from java.lang import System
from java.io import File
from test_base import TestBase

class TestCharacterClassifier(TestBase):
    '''
    A tester for the word classifer
    '''
    
    def test_init_method(self):
        '''Test with different number of training examples and compare
        random init with count based init'''
        
        test_dir = File("../../character_examples").getPath()
        nr_of_training_examples = 90
        nr_of_test_examples = 10
        
        extracor = SimpleImageFeatureExtractor(nr_of_divisions=7, 
                                               size_classification_factor=1.3)
        
        training_examples, test_examples = extracor.extract_training_and_test_examples(test_dir, 
                                                                                       nr_of_training_examples, 
                                                                                       nr_of_test_examples)
        
        def get_examples(nr_of_examples):
            if(nr_of_examples!=90):
                raise "Illegal amount of examples"
            else:
                return training_examples
            
        
        def get_character_classifier_with_init_method(traing_examples, init_method):
            return CharacterClassifier(traing_examples,
                                       nr_of_hmms_to_try=1,
                                       fraction_of_examples_for_test=0,
                                       train_with_examples=False,
                                       initialisation_method=init_method)
        
        self.test_init_method_with_classifier(get_examples, 
                                              get_character_classifier_with_init_method,
                                              test_examples,
                                              [90])
        #With 90 training examples with letters A to H and 10 test examples for every letter
        #../../../../jython2.5.2/bin/jython -J-Xmx1024m character_classifier_tester.py 
        #('number of training examples', 'random init score before training', 'count based init score before training', 'random init score after training', 'count based init score after training', 'random init training time', 'count based init training time')
        #(90, 0.225, 0.7875, 0.4625, 0.3875, 136794L, 61550L)


if __name__ == "__main__":
    character_classifer_tester = TestCharacterClassifier()
    character_classifer_tester.test_init_method()