'''
Created on Jul 3, 2011

@author: kjell
'''

from random import random
from random import choice
import unittest

example_alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def generate_examples_for_word(word="dog", number_of_examples=100, poelap=0.03, poelenl=0.7, powlap=0.1, polmap=0.01, alphabet=example_alphabet):
    '''
    Function that generate misspelled versions of a word given propabilities
    defined by the parameters.  
        
    Parameters:
    word = the word that the examples shall be generated for
    poelap = probability of extra letter at position
    poelenl = probability of extra letter equals neighbor letter
    powlap = probability of wrong letter at position
    polmap = probability of letter missing at position
    number_of_examples = the number of examples that shall be generated
    
    Returns:
    A list of size number_of_examples containing versions of the word
    '''
    #Help functions:
    def true_with_probability(probability):
        return random() <= probability
    
    def neighbors_at_position(word, position):
        word_length = len(word)
        if(position==0):
            return [word[0]]
        elif position < word_length:
            return [word[position-1], word[position]]
        else:
            return [word[word_length-1]]
    
    def actual_or_other(letter):
        if(true_with_probability(polmap)):#Letter missing at position
            return ""
        else:
            if(true_with_probability(powlap)):#Wrong letter at position
                return choice(alphabet)
            else:
                return letter        
    
    def generate_example_for_word_from_pos(word,start_at_position=0):
        if start_at_position > len(word):
            return ""
        else:
            end = start_at_position == len(word)
            char_at_pos = "" if end else actual_or_other(word[start_at_position])
            rest = generate_example_for_word_from_pos(word,start_at_position+1)
            if(true_with_probability(poelap)):#probability of extra letter 
                if(true_with_probability(poelenl)):#probability of extra letter equals to neighbor
                    neighbor = choice(neighbors_at_position(word, start_at_position))
                    return neighbor + char_at_pos + rest
                else:
                    extra_letter = choice(alphabet)
                    return extra_letter + char_at_pos + rest
            else:
                return char_at_pos + rest
        
    #Generate the examples
    examples = []
    for i in range(number_of_examples): #@UnusedVariable
        examples.append(generate_example_for_word_from_pos(word))
    return examples


default_word_list = ["dog","cat","pig","love","hate",
                     "scala","python","summer","winter","night",
                     "daydream","nightmare","animal","happiness","sadness",
                     "friendliness","feminism","fascism","socialism","capitalism"]

def generate_examples_for_words(words=default_word_list, number_of_examples=100, poelap=0.03, poelenl=0.7, powlap=0.1, polmap=0.01, alphabet=example_alphabet):
    '''
    Generate tuples for all words in the list words of the format:
    (word, list of training examples for the words)
    
    See generate_examples_for_word for description of the rest of the parameters
    '''
    word_training_example_tuples = []
    for word in words:
        word_training_example_tuples.append((word,generate_examples_for_word(word, number_of_examples, poelap, poelenl, powlap, polmap, alphabet)))
    return word_training_example_tuples

class TestWordExampleGenerator(unittest.TestCase):

    def test_word_example_generator(self):
        print(generate_examples_for_word(word="dog",number_of_examples=100))
        pass
    
    def test_words_example_generator(self):
        print(generate_examples_for_words(words=default_word_list,number_of_examples=100))
        pass


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()

        
            