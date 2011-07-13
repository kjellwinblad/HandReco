'''
Created on Jul 10, 2011

@author: kjell
'''
from api.word_hmm import WordHMM
from api.word_examples_generator import generate_examples_for_words
from api.specialized_hmm import SpecializedHMM
import unittest


class WordClassifier(object):
    '''
    Classifies a possible misspelled word to a word
    '''


    def __init__(self, 
                 words_with_examples, 
                 nr_of_hmms_to_try = 3, 
                 fraction_of_examples_for_test = 0.1):
        '''
        Parameters:
        words_with_examples - is a list of tuples were the first element in the tuples
        is a string representing a word that the classifier should handle and the second
        element is a list of training examples for that word.
        nr_of_hmms_to_try - creates nr_of_hmms_to_try hmms for each word and selects the one with
        highest probability for the test examples
        fraction_of_examples_for_test -  fraction of the training examples that will be used for test
        All training examples will be used for both test and training if it is set to 0
        '''
        self.words = []
        self.hmms_for_words = []
        for word,training_examples in words_with_examples:
            self.words.append(word)
            test_examples = []
            actual_training_examples = []
            if(fraction_of_examples_for_test == 0):
                test_examples = training_examples
                actual_training_examples = training_examples
            else:
                change_pot_at = len(training_examples)*fraction_of_examples_for_test
                for i in range(len(training_examples)):
                    if(i<change_pot_at):
                        test_examples.append(training_examples[i])
                    else:
                        actual_training_examples.append(training_examples[i])
                
            word_hmm = self.create_hmm_for_word(word, 
                                                actual_training_examples,
                                                test_examples,
                                                nr_of_hmms_to_try)
            self.hmms_for_words.append(word_hmm)
    
    
    def create_hmm_for_word(self, word, training_examples, test_examples, nr_of_hmms_to_try):
        #Create nr_of_hmms_to_try hmms and select the one with the best result
        results=[]
        hmms=[]
        for i in range(nr_of_hmms_to_try):
            hmm = WordHMM(word, 
                          SpecializedHMM.InitMethod.count_based,
                          training_examples)
            try:
                hmm.train_until_stop_condition_reached(training_examples, 0.0, test_examples)
            except ZeroDivisionError:
                print("Divide by zero while training")
            hmms.append(hmm)
            result = hmm.test(test_examples)
            results.append(result)
            print("hmm " + str(i) + " for word " + word + " result " + str(result))
        max_result = max(results)
        print("max hmm for word " + word + " max result " + str(max_result))
        return hmms[results.index(max_result)]
    
    def classify(self,string):
        scores = []
        for hmm in self.hmms_for_words:
            score = hmm.test([string])
            scores.append(score)
        max_score = max(scores)
        return self.words[scores.index(max_score)]


class TestWordClassifier(unittest.TestCase):

    def test_create_classifier(self):
        examples = generate_examples_for_words(number_of_examples=70)
        classifier = WordClassifier(examples, nr_of_hmms_to_try = 1, fraction_of_examples_for_test = 0)
        print("classification of dog " + classifier.classify("dog"))
        print("classification of dag " + classifier.classify("dag"))
        print("classification of cat " + classifier.classify("cat"))
        print("classification of catt " + classifier.classify("catt"))
        print("classification of animal " + classifier.classify("animal"))
        print("classification of aoimal " + classifier.classify("aoimal"))
        print("classification of feminismm " + classifier.classify("feminismm"))
        print("classification of socialism " + classifier.classify("socialism"))
        print("classification of socialisa " + classifier.classify("socialisa"))
        print("classification of capitalism " + classifier.classify("capitalism"))
        print("classification of ccapitalism " + classifier.classify("cxapitalism"))
        print("classification of friendliness " + classifier.classify("friendliness"))
        print("classification of friendlinesss " + classifier.classify("friendlinesss"))
        print("classification of python " + classifier.classify("python"))
        print("classification of pythona " + classifier.classify("pythona"))
        print("classification of summer " + classifier.classify("summer"))
        print("classification of sumer " + classifier.classify("sumer"))
        pass
        #["dog","cat","pig","love","hate",
        #             "scala","python","summer","winter","night",
        #             "daydream","nightmare","animal","happiness","sadness",
        #             "friendliness","feminism","fascism","socialism","capitalism"]


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()
        
            
        