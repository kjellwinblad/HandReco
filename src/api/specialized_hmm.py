'''
Created on Jul 7, 2011

@author: kjellw
'''
from random import random
from hmm import HMM
import unittest

def random_list_with_sum(number_of_elements, sum):
    def random_list_with_sum_int(number_of_elements_left, list_so_far):
        if(number_of_elements_left<=0):
            return list_so_far
        else:
            max_value = max(list_so_far)
            new_number1 = max_value*random()
            new_number2 = max_value - new_number1
            del list_so_far[list_so_far.index(max_value)]
            list_so_far.append(new_number1)
            list_so_far.append(new_number2)
            return random_list_with_sum_int(number_of_elements_left-1, list_so_far)
    
    if(number_of_elements==0):
        return []
    else:        
        return random_list_with_sum_int(number_of_elements-1, [sum])

def fill_list_with_zeros_in_beginning_to_size(list, size):
    if(len(list)==size):
        return list
    elif(len(list)<size):
        list.insert(0,0)
        return fill_list_with_zeros_in_beginning_to_size(list, size)
    else:
        del list[len(list)-1]
        return fill_list_with_zeros_in_beginning_to_size(list, size)
    
def zeros_and_random_with_sum1(size, number_of_randoms):
    rl = random_list_with_sum(number_of_randoms,1.0)
    return fill_list_with_zeros_in_beginning_to_size(rl,size)
    
def zeros(number_of_zeros):
    l = []
    for i in range(number_of_zeros):
        l.append(0)
    return l



class SpecializedHMM(HMM):
    '''
    classdocs
    '''

    class InitMethod:
        random = 0
        uniform = 1
        count_based = 2

    def __init__(self, pi, A, B, V):
        super(HMM,self).__init__(pi, A, B, V)
        
        
class TestHMM(unittest.TestCase):

    def test_zeros_and_random_with_sum1(self):
        r = zeros_and_random_with_sum1(10, 5)
        print(r)
        if((sum(r)>0.9) and (sum(r)<1.1) and r[4]==0):
            pass
        else:
            raise "fail"
    
    def test_random_list_with_sum(self):
        r = random_list_with_sum(5, 1)
        print(r)
        if((sum(r)>0.9) and (sum(r)<1.1)):
            pass
        else:
            raise "fail"
        
if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_word_']
    unittest.main()
        