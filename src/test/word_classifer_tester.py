'''
Created on Jul 17, 2011

@author: kjell
'''
import sys
sys.path.append("../gui")
sys.path.append("../api")
sys.path.append("..")

from api.word_examples_generator import generate_examples_for_words
from api.word_classifier import WordClassifier
from api.specialized_hmm import SpecializedHMM
from java.lang import System
from test_base import TestBase

class TestWordClassifier(TestBase):
    '''
    A tester for the word classifer
    '''
    
    def test_init_method(self):
        '''Test with different number of training examples and compare
        random init with count based init'''
        word_list = ["dog","cat","pig","love","hate",
                     "scala","python","summer","winter","night",
                     "daydream","nightmare","animal","happiness","sadness",
                     "tennis","feminism","fascism","socialism","capitalism"]
        
        def get_examples(nr_of_examples):
            return generate_examples_for_words(words=word_list,
                                               number_of_examples=nr_of_examples,
                                               poelap=0.03,
                                               poelenl=0.7,
                                               powlap=0.1,
                                               polmap=0.03)
        
        def get_word_classifier_with_init_method(traing_examples, init_method):
            return WordClassifier(traing_examples,
                                  nr_of_hmms_to_try=1,
                                  fraction_of_examples_for_test=0,
                                  train_with_examples=False,
                                  initialisation_method=init_method)
        
        nr_of_test_examples=5
        
        test_examples = get_examples(nr_of_test_examples)
        
        
        self.test_init_method_with_classifier(get_examples, 
                                              get_word_classifier_with_init_method,
                                              test_examples,
                                              [100,200,400,800,1600,3200,6400,12800])
        
            #../../../../jython2.5.2/bin/jython -J-Xmx1024m word_classifer_tester.py 
            #('number of training examples', 'random init score before training', 'count based init score before training', 'random init score after training', 'count based init score after training', 'random init training time', 'count based init training time')
            #(100, 0.03, 0.99, 0.01, 0.0, 347825L, 195169L)
            #(200, 0.02, 1.0, 0.13, 0.36, 713612L, 315888L)
            #(400, 0.02, 1.0, 0.9, 0.95, 1384908L, 416520L)
            #(800, 0.01, 1.0, 1.0, 1.0, 2778273L, 790979L)
            #(1600, 0.05, 1.0, 1.0, 1.0, 5735563L, 1580539L)
            #Divide by zero while training
            #Divide by zero while training
            #Divide by zero while training
            #Divide by zero while training
            #(3200, 0.11, 1.0, 0.94, 1.0, 11165581L, 3105260L)


if __name__ == "__main__":
    word_classifer_tester = TestWordClassifier()
    word_classifer_tester.test_init_method()