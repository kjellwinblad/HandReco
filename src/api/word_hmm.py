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
from word_examples_generator import generate_examples_for_word

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
        #Set of emission symbols
        V = ['@'] + get_example_alphabet() + ['$']
        #Initial state
        pi = zeros(self.number_of_states)
        pi[0] = 1
        super(WordHMM,self).__init__(pi, A, B, V)
    
    def observation_from_word(self,word):
        word_with_special_start_and_end = "@" +  word +  "$"
        observation_list = []
        for letter in word_with_special_start_and_end:
            observation_list.append(self.V.index(letter))
        return observation_list
    
    def train(self, training_examples):
        observation_list = []
        for word in training_examples:
            observation_list = observation_list + self.observation_from_word(word)
        self.baum_welch(observation_list)
        
    def test(self, word_list):
        '''Returns the likelihood of the word given the model'''
        probabilities_for_words = []
        for word in word_list:
            O = self.observation_from_word(word)
            alpha_matrix = self.calc_forward(O)
            last_row = alpha_matrix[len(alpha_matrix)-1]
            probabilities_for_words.append(sum(last_row))
        average = sum(probabilities_for_words)/len(probabilities_for_words)
        return average
         

class TestHMM(unittest.TestCase):
    
    
    def test_with_word(self):
        ''' not yet implemented'''
        word_hmm = WordHMM("dog")
        if len(word_hmm.A) == 5:
            pass
        else:
            raise "The size of A is incorrect"
    
    def test_train(self):
        ''' not yet implemented'''
        word_hmm = WordHMM("dog")
        examples = generate_examples_for_word(word="dog", number_of_examples=30)
        test_examples = generate_examples_for_word(word="dog", number_of_examples=10)
        other_test_examples = generate_examples_for_word(word="pig", number_of_examples=10)
        before = word_hmm.test(test_examples)
        word_hmm.train(examples)
        after = word_hmm.test(test_examples)
        other_test_examples_test = word_hmm.test(other_test_examples)
        
        print(["before", before, "after", after,"other_test_examples_test", other_test_examples_test])
        
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()