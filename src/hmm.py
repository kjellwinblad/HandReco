import unittest
import logging
import random

def zeros_3d(x, y, z):
    matrix = []
    for i in range(x):
        matrix.append(zeros(y,z))
    return matrix

def zeros(x, y):
    ''' Return a matrix of zeros with height x and width y. '''
    matrix = []
    for i in range(x):
        matrix.append([0] * y)
    return matrix



def select_random(massDist):
    ''' Given a discrete distribution, for example [0.2, 0.5, 0.3], select an element.
        Note that the probabilities need to sum up to 1.0
    '''
    assert(sum(massDist) == 1.0)
    randRoll = random.random() # in [0,1)
    s = 0
    result = 0
    for mass in massDist:
        s += mass
        if randRoll < s:
            return result
        result+=1


class HMM:
    # Variables, the notation is the same as in the Rabiner paper.
    # A = State Transition probability
    # B = Observation Probability Distribution
    # V = Vocabulary of observations
    # pi = Initial State distribution
    # N = Number of States
    # K = Number of symbols in vocabulary
    # q = current state
    # t = current (discrete) time

    def __init__(self, pi, A, B, V):
        ''' Initalize the HMM with the supplied values'''
        self.pi = pi
        self.A = A
        self.N = len(A[0])
        self.B = B
        self.V = V
        self.K = len(V)
        self.q = select_random(self.pi)
        self.t = 0
        self.O = []
        self.log = logging.getLogger('log')
        logging.basicConfig()
        self.log.debug(' Time is ' + str(self.t) + ', Initial State is ' + str(self.q) + ', Sequence is ' + str(self.O))

    def gen(self):
        '''Generate a new observation based on the current state and transition to a new state.'''
        index = select_random(self.B[self.q])
        observation = self.V[index]
        self.O.append(observation)
        self.q = select_random(self.A[self.q])
        self.t += 1
        self.log.debug(' Time is ' + str(self.t) + ', Observed ' + observation + ', New State is ' + str(self.q) + ', Sequence is ' + str(self.O))

    def calc_forward(self, O):
        T = len(O)
        print 'T =', T
        self.alpha = zeros(T, self.N)
        #initalize
        t = 0
        for i in range(self.N):
            self.alpha[t][i] = pi[i] * B[i][O[t]]
        print self.alpha
        #induction
        for t in range(1,T):
            for j in range(self.N):
                prob_sum = 0
                for i in range(self.N):
                    prob_sum += self.alpha[t-1][i] * A[i][j]
                self.log.debug('t is ' + str(t) + ', i = ' + str(i) + ', j = ' +str(j) + ', O[t] = ' + str(O[t]) + ', prob_sum = ' + str(prob_sum) + ', B[j][O[t]] = ' + str(B[j][O[t]]))
                self.alpha[t][j] = prob_sum * B[j][O[t]]
        print self.alpha
        final_prob = 0
        for i in range(self.N):
            final_prob += self.alpha[T-1][i]
        print final_prob

    def calc_backward(self, O):
        T = len(O)
        self.beta = zeros(T, self.N)
        #initialization
        for i in range(self.N):
            self.beta[T-1][i] = 1
        self.log.debug(' beta is ' + str(self.beta))
        print 'inital beta ', self.beta
        #induction
        for t in range(T-2, -1, -1):
            for i in range(self.N):
                prob_sum = 0
                for j in range(self.N):
                    prob_sum += self.A[i][j] * self.B[j][O[t]] * self.beta[t+1][j]
                self.beta[t][i] = prob_sum
        self.log.debug(' beta is ' + str(self.beta))

    def viterbi(self, O):
        T = len(O)
        delta = zeros(T, self.N)
        psi = zeros(T, self.N)
        #initialization
        t = 0
        for i in range(self.N):
            delta[t][i] = pi[i] * B[i][O[t]]
            psi[t][i] = 0
        # recursion
        for t in range(1, T):
            for j in range(self.N):
                acc = []
                for i in range(self.N):
                    acc.append(delta[t-1][i] * A[i][j])
                delta[t][j] = max(acc) * B[j][O[t]]
                psi[t][j] = acc.index(max(acc))
        print delta
        print psi

    def baum_welch(self, O):
        # We need to calculate the xi and gamma tables before can find the update values
        xi = zeros_3d(len(O) - 1, self.N, self.N)
        gamma = zeros(len(O) - 1, self.N)
        print 'xi ', xi
        # Begin with xi
        for t in range(len(O) - 1):
            s = 0
            for i in range(self.N):
                for j in range(self.N):
                    self.log.debug(' t = ' + str(t) + ', i = ' + str(i) + ', j = ' +str(j))
                    xi[t][i][j] = self.alpha[t][i] * self.A[i][j] * self.B[j][O[t+1]] * self.beta[t+1][j]
                    s += xi[t][i][j]
            # Normalize
            for i in range(self.N):
                for j in range(self.N):
                    xi[t][i][j] *= 1/s
        print xi

        # Now calculate the gamma table
        for t in range(len(O) - 1):
            for i in range(self.N):
                s = 0
                for j in range(self.N):
                    s += xi[t][i][j]
                gamma[t][i] = s
        print gamma
        # Update model parameters
        # Update pi
        for i in range(self.N):
            pi[i] = gamma[0][i]
        # Update A
        for i in range(self.N):
            for j in range(self.N):
                numerator = 0
                denominator = 0
                for t in range(len(O) - 1):
                    numerator += xi[t][i][j]
                    denominator += gamma[t][i]
                self.A[i][j] = numerator / denominator
        # Update B
        for j in range(self.N):
            for k in range(self.K):
                numerator = 0
                denominator = 0
                for t in range(len(O) - 1):
                    if O[t] == k:
                        numerator += gamma[t][j]
                    denominator += gamma[t][j]
                B[j][k] = numerator / denominator
                
# Vocabulary
V = ['a', 'b']
# initial state probabilities
pi = [0.5, 0.5]
# row index is current state, column index is new state
# i.e. in state 0 we have 80% chance of staying in state 0 and 20% of transitioning to state 1
A = [[0.8, 0.2],
     [0.1, 0.9]]
# row index is state, column index is observation
# i.e. in state 0 we can only observe 'a' and in state 1 we can only observe 'b'
B = [[1.0, 0.0],
     [0.0, 1.0]]

class TestHMM(unittest.TestCase):
    def test_zeros(self):
        ''' Test the zeros function '''
        self.assertEqual(zeros(2,2), [[0,0], [0,0]])
        self.assertEqual(zeros(3,1), [[0],[0],[0]])
        self.assertEqual(zeros(3,2), [[0,0], [0,0],[0,0]])

    def test_generate(self):
        '''Create a HMM and generate 100 observations'''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        for i in range(100):
            h.gen()

    def test_forward(self):
        ''' fixme '''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.calc_forward([0, 0])

    def test_backward(self):
        '''fixme '''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.calc_backward([0, 0])

    def test_viterbi(self):
        '''fixme'''
        h = HMM(pi, A, B, V)
        h.log.setLevel(logging.DEBUG)
        h.viterbi([0, 0])

if __name__ == '__main__':
    unittest.main()

test
