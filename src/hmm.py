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
        self.N = A[0].size
        self.B = B
        self.V = V
        self.q = select_random(self.pi)
        self.t = 0
        self.O = []
        self.log = logging.getLogger('log')
        logging.basicConfig()
        self.log.debug(' Time is ' + str(self.t) + ', Initial State is ' + str(self.q) + ', Sequence is ' + str(self.O))

    def calc_forward(self, O):
        T = O.size
        print 'T =', T
        alpha = numpy.zeros([T, self.N])
        #initalize
        t = 0
        for i in range(self.N):
            alpha[t, i] = pi[i] * B[i,O[t]]
        print alpha
        #induction
        for t in range(1,T):
            for j in range(self.N):
                prob_sum = 0
                for i in range(self.N):
                    prob_sum += alpha[t-1, i] * A[i, j]
                alpha[t, j] = prob_sum * B[j, O[t]]
        print alpha
        final_prob = 0
        for i in range(self.N):
            final_prob += alpha[T-1, i]
        print final_prob

    def calc_backward(self, O):
        T = O.size
        beta = numpy.zeros([T, self.N])
        #initialization
        for i in range(self.N):
            beta[T-1, i] = 1
        print 'inital beta ', beta
        #induction
        for t in range(T-2, -1, -1):
            for i in range(self.N):
                prob_sum = 0
                for j in range(self.N):
                    prob_sum += self.A[i, j] * self.B[j, O[t]] * beta[t+1, j]
                beta[t, i] = prob_sum

    def gen(self):
        '''Generate a new observation based on the current state'''
        index = select_random(self.B[self.q])
        observation = self.V[index]
        self.O.append(observation)
        self.q = select_random(self.A[self.q])
        self.t += 1
        self.log.debug(' Time is ' + str(self.t) + ', Observed ' + observation + ', New State is ' + str(self.q) + ', Sequence is ' + str(self.O))

    def viterbi(self, O):
        T = O.size
        delta = numpy.zeros([T, self.N])
        psi = numpy.zeros([T, self.N])
        #initialization
        t = 0
        for i in range(self.N):
            delta[t, i] = pi[i] * B[i, O[t]]
            psi[t, i] = 0
        # recursion
        for t in range(1, T):
            for j in range(self.N):
                acc = []
                for i in range(self.N):
                    acc.append(delta[t-1, i] * A[i, j])
                delta[t, j] = max(acc) * B[j, O[t]]
                psi[t, j] = acc.index(max(acc))
        print delta
        print psi

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

class TestHMM(unittest.TestCase):
    def generate(self):
        '''Create a HMM and generate 100 observations'''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        for i in range(100):
            h.gen()

    def forward(self):
        ''' fixme '''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.calc_forward(numpy.array([0, 0]))

    def backward(self):
        '''fixme '''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.calc_backward(numpy.array([0, 0]))

    def viterbi(self):
        '''fixme'''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.viterbi(numpy.array([0, 0]))

if __name__ == '__main__':
    unittest.main()
