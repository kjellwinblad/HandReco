'''
Created on Jul 19, 2011

@author: kjell
'''
from api.specialized_hmm import SpecializedHMM
from java.lang import System

class TestBase(object):
    '''
    A base class for tests with some common methods
    '''
    
    def test_init_method_with_classifier(self, 
                                         get_examples, 
                                         get_classifier_with_init_method,
                                         test_examples,
                                         nr_of_examples_to_test_list,
                                         only_count_based_init=False):
        print("number of training examples",
              "random init score before training",
              "count based init score before training",
              "random init score after training",
              "count based init score after training",
              "random init training time",
              "count based init training time")
        
        for nr_of_training_examples in nr_of_examples_to_test_list:
            training_exampels = get_examples(nr_of_training_examples)
            if not only_count_based_init:
                random_init_classifer = get_classifier_with_init_method(training_exampels,
                                                                        SpecializedHMM.InitMethod.random)
            count_based_init_classifer = get_classifier_with_init_method(training_exampels,
                                                                         SpecializedHMM.InitMethod.count_based)
            #Before training
            if not only_count_based_init:
                random_score_before_training = random_init_classifer.test(test_examples)
            else:
                random_score_before_training = None
            count_score_before_training = count_based_init_classifer.test(test_examples)
            #Train
            start_time = System.currentTimeMillis()
            if not only_count_based_init:
                random_init_classifer.train(training_exampels)
            random_init_training_time = System.currentTimeMillis() - start_time
            start_time = System.currentTimeMillis()
            count_based_init_classifer.train(training_exampels)
            count_based_init_training_time = System.currentTimeMillis() - start_time
            #After training
            if not only_count_based_init:
                random_score_after_training = random_init_classifer.test(test_examples)
            else:
                random_score_after_training = None
            count_score_after_training = count_based_init_classifer.test(test_examples)
            print(nr_of_training_examples,
                  random_score_before_training,
                  count_score_before_training,
                  random_score_after_training,
                  count_score_after_training,
                  random_init_training_time,
                  count_based_init_training_time)

    

        