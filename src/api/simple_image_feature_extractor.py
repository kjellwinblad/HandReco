'''
Created on Jul 18, 2011

@author: kjell
'''

class SimpleImageFeatureExtractor(object):
    '''
    A class used to extract a sequence of features from an image that
    may be used as training observations for a HMM.
    '''


    def __init__(self,nr_of_divisions):
        '''
        Parameters:
        nr_of_divisions - Number of times to divide the image vertically 
        '''
        self.nr_of_divisions = nr_of_divisions
        
    
        