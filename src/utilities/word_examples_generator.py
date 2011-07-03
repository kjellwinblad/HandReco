'''
Created on Jul 3, 2011

@author: kjell
'''

from random import random
from random import choice

example_alphabet=['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

def generate_examples_for_word(word="dog", number_of_examples=100, poelap=0.05, poelenl=0.5, powlap=0.2, alphabet=example_alphabet):
    '''
    Function that generate misspelled versions of a word given propabilities
    defined by the parameters.  
        
    Parameters:
    word = the word that the examples shall be generated for
    poelap = probability of extra letter at position
    poelenl = probability of extra letter equals neighbor letter
    powlap = probability of wrong letter at position
    number_of_examples = the number of examples that shall be generated
    
    Returns:
    A list of size number_of_examples containing versions of the word
    '''
    
    def true_with_probability(probability):
        return random() <= probability
    
    def generate_example_for_word(word, poelap, poelenl, powlap):
        def neighbors_at_position(word, position):
            word_length = len(word)
            if(position==0):
                return [word[0]]
            elif(position==word_length):
                return [word[word_length-1]]
            else:
                [word[position], word[position+1]]
        
        def word_with_letters_inserted_at_random(word,start_at_position=0):
            if start_at_position==(len(word)+1):
                return ""
            else:
                def actual_or_other(letter):
                    if(true_with_probability(powlap)):
                        return choice(alphabet)
                    else:
                        return letter
                    
                end = start_at_position==len(word)
                char_at_pos = "" if end else actual_or_other(word[start_at_position])
                rest = word_with_letters_inserted_at_random(word,start_at_position+1)
                if(true_with_probability(poelap)):#probability of extra letter 
                    if(true_with_probability(poelenl)):#probability of extra letter equals to neighbor
                        neighbor = choice(neighbors_at_position(word, start_at_position))
                        return neighbor + char_at_pos + rest
                    else:
                        extra_letter = choice(alphabet)
                        return extra_letter + char_at_pos + rest
                else:
                    return char_at_pos + rest
        
        
        