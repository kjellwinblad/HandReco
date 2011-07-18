'''
Created on Jul 18, 2011

@author: kjell
'''
from api.word_classifier import WordClassifier
from api.specialized_hmm import SpecializedHMM
from api import simple_image_feature_extractor
from api.simple_image_feature_extractor import SimpleImageFeatureExtractor
from java.io import File
import shutil
import unittest

class CharacterClassifier(WordClassifier):
    '''
    Works as WordClassifier with some extra features for character classification
    '''


    def __init__(self,
                 characters_with_examples,
                 nr_of_hmms_to_try=3,
                 fraction_of_examples_for_test=0.1,
                 train_with_examples=True,
                 initialisation_method=SpecializedHMM.InitMethod.count_based):
        '''
        See WordClassifier
        '''
        #Get the number of segments created by the feature extractor
        #by looking at the length of a training example
        label,examples = characters_with_examples[0]
        self.nr_of_segments = len(examples[0])
        new_characters_with_examples = []
        for label,examples in characters_with_examples:
            new_characters_with_examples.append((label*self.nr_of_segments,examples))
        super(CharacterClassifier,self).__init__(new_characters_with_examples,
                                                 nr_of_hmms_to_try,
                                                 fraction_of_examples_for_test,
                                                 train_with_examples,
                                                 initialisation_method,
                                                 alphabet=SimpleImageFeatureExtractor.feature_ids)
    
    def test(self,test_examples):
        '''
        See WordClassifier.test()
        '''
        new_test_examples = []
        for label, examples in test_examples:
            new_test_examples.append((label * self.nr_of_segments, examples))
        return super(CharacterClassifier, self).test(new_test_examples)
        
        
class TestCharacterClassifier(unittest.TestCase):
    
    def test_with_two_characters(self):
        #test with just two letters so A and B are copied to a 
        #special dir that is deleted after the test
        base_dir = File("../../character_examples")
        test_dir = File(base_dir,"test")
        a_dir = File(base_dir,"A")
        b_dir = File(base_dir,"B")
        shutil.copytree(a_dir.getPath(), File(test_dir,"A").getPath())
        shutil.copytree(b_dir.getPath(), File(test_dir,"B").getPath())
        print("files copied")
        extracor = SimpleImageFeatureExtractor(nr_of_divisions=7, 
                                               size_classification_factor=1.3)
        #Extract features
        training_examples, test_examples = extracor.extract_training_and_test_examples(test_dir.getPath(), 90, 10)
        print("training examples", training_examples)
        print("testing examples", test_examples)
        classifier = CharacterClassifier(training_examples, 
                                         nr_of_hmms_to_try = 1, 
                                         fraction_of_examples_for_test = 0.3,
                                         train_with_examples=False)
        before = classifier.test(test_examples)
        classifier.train()
        after = classifier.test(test_examples)
        print("test_with_two_characters", "before", before, "after", after)
        shutil.rmtree(test_dir.getPath())

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()
        