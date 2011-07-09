'''
Created on Jul 7, 2011

@author: kjellw
'''

from hmm import HMM
from specialized_hmm import SpecializedHMM
from specialized_hmm import zeros
from specialized_hmm import random_list_with_sum
from specialized_hmm import fill_list_with_zeros_in_beginning_to_size
from specialized_hmm import zeros_and_random_with_sum1
from word_examples_generator import get_example_alphabet

import unittest
from specialized_hmm import SpecializedHMM 

class WordHMM(SpecializedHMM):
    '''
    A HMM that represent a sequence of letter that form a word.
    It is implemented in the way described in the paper:
    Initial model selection for the Baum-Welch algorithm as applied to 
    HMMs of DNA sequences.
    '''
    
    def init_row(self, row_index):
        if(self.init_method==SpecializedHMM.InitMethod.random):
            return zeros_and_random_with_sum1(self.number_of_states, self.number_of_states-row_index)
        else:
            raise "Init Method Not Supported"

    def __init__(self, word, init_method=SpecializedHMM.InitMethod.random, training_examples=[]):
        '''
        Training examples is only used if InitMethod.count_based is used
        '''
        print("running")
        self.word = word
        self.init_method = init_method
        #Construct the state transition matrix
        self.number_of_states = len(word) + 2
        #state transition matrix
        A = []
        #From state 1 to state 2 the probability is 
        state1 = zeros(self.number_of_states)
        state1[1]=1
        A.append(state1)
        for i in range(1,self.number_of_states-1):
            state_row = self.init_row(i)
            A.append(state_row)
        #last state can only be transfered to state1 with probability 1
        last_state = zeros(self.number_of_states)
        last_state[0]=1
        A.append(last_state)
        print(A)
        #init state emission probabilities...
        number_of_emissions = len(get_example_alphabet()) + 2
        B = []
        #init the first row with specific probability for @
        B.append(zeros(number_of_emissions))
        B[0][0] = 1
        #init the rest emission probabilities without the last row
        for i in range(1, self.number_of_states-1):
            B.append(zeros(number_of_emissions))
            B[i] = random_list_with_sum(number_of_emissions, 1)
            B[i][0] = 0 
            B[i][number_of_emissions-1] = 0
        #init the last row for specific probability for $
        B.append(zeros(number_of_emissions))
        B[self.number_of_states-1][number_of_emissions-1]=1
        for row in B:
            print(row)             
        #super(HMM,self).__init__(pi, A, B, V)

    
class TestHMM(unittest.TestCase):
    
    def test_with_word(self):
        ''' not yet implemented'''
        WordHMM("dog")
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()