import unittest
import numpy
import logging

def select_random(distribution):
    '''Given an array specifying the discrete distribution, select a value and return the index'''
    res = numpy.random.multinomial(1, distribution)
    for i in range(res.size):
        if res[i] == 1:
            return i
    
class HMM:
    # Variables, the notation is the same as in the Rabiner paper.
    # A = State Transition probability
    # B = Observation Probability Distribution
    # V = Vocabulary of observations
    # pi = Initial State distribution
    # q = current state
    # t = current (discrete) time

    def __init__(self, pi, A, B, V):
        ''' Initalize the HMM with the supplied values'''
        self.pi = pi
        self.A = A
        self.B = B
        self.V = V
        self.q = select_random(self.pi)
        self.t = 1
        self.O = []
        self.log = logging.getLogger('log')
        logging.basicConfig()
        self.log.debug(' Time is ' + str(self.t) + ', Initial State is ' + str(self.q) + ', Sequence is ' + str(self.O))

    def gen(self):
        '''Generate a new observation based on the current state'''
        index = select_random(self.B[self.q])
        observation = self.V[index]
        self.O.append(observation)
        self.q = select_random(self.A[self.q])
        self.t += 1
        self.log.debug(' Time is ' + str(self.t) + ', Observed ' + observation + ', New State is ' + str(self.q) + ', Sequence is ' + str(self.O))

class TestHMM(unittest.TestCase):
    def test(self):
        '''Create a HMM and generate 100 observations'''
        # Vocabulary
        V = ['a', 'b']
        # initial state probabilities
        pi = numpy.array([0.5, 0.5])
        # row index is current state, column index is new state
        # i.e. in state 0 we have 80% chance of staying in state 0 and 20% of transitioning to state 1
        A = numpy.array([[0.8, 0.2],
                         [0.1, 0.9]])
        # row index is state, column index is observation
        # i.e. in state 0 we can only observe 'a' and in state 1 we can only observe 'b'
        B = numpy.array([[1.0, 0.0],
                         [0.0, 1.0]])
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        for i in range(100):
            h.gen()

if __name__ == '__main__':
    unittest.main()
