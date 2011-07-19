import unittest
import logging
import random
import math

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


class HMM(object):
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
        self.scaling_factor = []
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
        self.scaling_factor = []
        T = len(O)
        alpha = zeros(T, self.N)
        #initalize
        t = 0  
        alpha[t] = [self.pi[i] * self.B[i][O[t]] for i in range(self.N)]   
        def append_scaling_to_scaling_factor_for_t(t):
            sum_alpha = sum(alpha[t-1])
            if(sum_alpha==0):
                self.scaling_factor.append(1)
            else:
                self.scaling_factor.append(1.0/sum_alpha)
        #induction         
        for t in range(1,T):
            append_scaling_to_scaling_factor_for_t(t)
            alpha[t-1] = [self.scaling_factor[-1] * alpha[t-1][i] for i in range(self.N)]
            for j in range(self.N):
                prob_sum = 0  
                for i in range(self.N):    
                    prob_sum += alpha[t-1][i] * self.A[i][j]
                self.log.debug('t is ' + str(t) + ', i = ' + str(i) + ', j = ' +str(j) + ', O[t] = ' + str(O[t]) + ', prob_sum = ' + str(prob_sum) + ', B[j][O[t]] = ' + str(self.B[j][O[t]]))
                alpha[t][j] = prob_sum * self.B[j][O[t]]
        append_scaling_to_scaling_factor_for_t(T)
        alpha[T-1] = [self.scaling_factor[-1] * alpha[T-1][i] for i in range(self.N)]
        return alpha

    def calc_backward(self, O):
        T = len(O)
        self.calc_forward(O)
        beta = zeros(T, self.N)
        scaling_factor = self.scaling_factor
        #initialization
        for i in range(self.N):
            beta[T-1][i] = 1.0
        self.log.debug(' beta is ' + str(beta))
        #induction
        for t in range(T-2, -1, -1):
            for i in range(self.N):
                prob_sum = 0
                for j in range(self.N):
                    #print('scaling_factor=' + str(scaling_factor))
                    prob_sum += self.A[i][j] * (scaling_factor[t+1] *self.B[j][O[t+1]]) * beta[t+1][j]
                beta[t][i] = prob_sum
        self.log.debug(' beta is ' + str(beta))
        return beta
    
    def probability_of_observation(self, O):
        """O is an observation sequence."""
        self.calc_forward(O)
        def log(x):
            return math.log10(x)
        try:
            log_of_probability = -sum(map(log, self.scaling_factor))
        except OverflowError:
            return 0.0
        probability = 10 ** log_of_probability
        return probability
        
        
    
    def viterbi(self, O):
        T = len(O)
        delta = zeros(T, self.N)
        psi = zeros(T, self.N)
        #initialization
        t = 0
        for i in range(self.N):
            #delta[t][i] = self.pi[i] * self.B[i][O[t]]
            delta[t][i] = math.log10(self.pi[i]) + math.log10(self.B[i][O[t]])
            psi[t][i] = 0
        # recursion
        for t in range(1, T):
            for j in range(self.N):
                acc = []
                for i in range(self.N):
                    acc.append(delta[t-1][i] + math.log10(self.A[i][j]))
                delta[t][j] = max(acc) + math.log10(self.B[j][O[t]])
                psi[t][j] = acc.index(max(acc))
        # path backtracking
        last_state = delta[T-1].index(max(delta[T-1]))
        path = [last_state]
        for t in range(T-1,0,-1):
            path.append(psi[t][path[-1]])
        path.reverse()
        return path
    
    def baum_welch(self, O):
        ''' Call with a sequence of observations, e.g. O = [0,1,0,1]. The function will
            calculate new model paramters according the baum welch formula. Will update
            pi.
        '''
        # Note, there is no scaling in this implementation !
        alpha = self.calc_forward(O)
        beta = self.calc_backward(O)

        # We need to calculate the xi and gamma tables before can find the update values
        xi = zeros_3d(len(O) - 1, self.N, self.N)
        gamma = zeros(len(O) - 1, self.N)
       
        # Begin with xi
        for t in range(len(O) - 1):
            s = 0
            for i in range(self.N):
                for j in range(self.N):
                    self.log.debug(' t = ' + str(t) + ', i = ' + str(i) + ', j = ' +str(j))
                    xi[t][i][j] = alpha[t][i] * self.A[i][j] * self.B[j][O[t+1]] * beta[t+1][j]
                    s += xi[t][i][j]
            # Normalize
            for i in range(self.N):
                for j in range(self.N):
                    xi[t][i][j] *= 1/s

        # Now calculate the gamma table
        for t in range(len(O) - 1):
            for i in range(self.N):
                s = 0
                for j in range(self.N):
                    s += xi[t][i][j]
                gamma[t][i] = s
        # Update model parameters
        # Update pi
        for i in range(self.N):
            self.pi[i] = gamma[0][i]
        # Update A
        #print 'Updating A'
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
                self.B[j][k] = numerator / denominator

    def baum_welch_bakis(self, O):
        ''' Call with a list of sequences of observations, e.g. O = [[0,1,0], [0,1,1]].
            This is an implemenation of equations 109 and 110 in Rabiner. Will NOT update
            pi as it assumed that the model is a bakis left-to-right model.'''
        alpha = []
        beta = []
        P = []
        K = len(O)
        
        for k in range(K):
            alpha.append(self.calc_forward(O[k]))
            beta.append(self.calc_backward(O[k]))
            final_prob = 0
            T = len(O[k])
            for i in range(self.N):
                final_prob += alpha[k][T-1][i]
            P.append(final_prob)
        # Update A
        for i in range(self.N):
            for j in range(self.N):
                sum_numerator = 0
                sum_denominator = 0
                for k in range(K):
                    # Calculate the numerator
                    T = len(O[k])
                    s = 0
                    for t in range(T - 1):
                        s += alpha[k][t][i] * self.A[i][j] * self.B[j][O[k][t+1]] * beta[k][t+1][j]
                    sum_numerator += 1.0 / P[k] * s
                    # Calculate the denominator
                    s = 0
                    for t in range(T - 1):
                        s += alpha[k][t][i] * beta[k][t][i]
                    sum_denominator += 1.0 / P[k] * s
                if sum_numerator == 0.0:
                    self.A[i][j] = 0.0
                else:
                    self.A[i][j] = sum_numerator / sum_denominator

        # Update B
        for j in range(self.N):
            for l in range(self.K):
                sum_numerator = 0
                sum_denominator = 0
                for k in range(K):
                    # Calculate the numerator
                    T = len(O[k])
                    s = 0.0
                    for t in range(T - 1):
                        if O[k][t] == l:
                            s += alpha[k][t][j] * beta[k][t][j]
                    sum_numerator += 1.0 / P[k] * s
                    # Calculate the denominator
                    s = 0.0
                    for t in range(T - 1):
                        s += alpha[k][t][j] * beta[k][t][j]
                    sum_denominator += 1.0 / P[k] * s
                if sum_numerator == 0.0:
                    self.B[j][l] = 0.0
                else:
                    self.B[j][l] = sum_numerator / sum_denominator

        # We don't need to update because we are assuming a bakis HMM where one state will have pi[i] = 1.0
    
    def to_string(self):
        '''
        Returns a string representation of the HMM that can be used
        to recreate the HMM with the from string class method
        '''
        return str((self.pi, self.A, self.B, self.V))
    
    @classmethod
    def from_string(cls, string):
        ''' Initalize the HMM with the HMM from string representation created with to_string'''
        pi, A, B, V = eval(string)
        return cls(pi, A, B, V)
        

class TestHMM(unittest.TestCase):
    def setUp(self):
        # Vocabulary
        self.V = ['a', 'b']
        # initial state probabilities
        self.pi = [0.5, 0.5]
        # row index is current state, column index is new state
        # i.e. in state 0 we have 80% chance of staying in state 0 and 20% of transitioning to state 1
        self.A = [[0.8, 0.2],
                  [0.1, 0.9]]
        # row index is state, column index is observation
        # i.e. in state 0 we can only observe 'a' and in state 1 we can only observe 'b'
        # when the element inside B is larger than 0, there's no domain error for log,
        # what if, we have 0.0 for some of the elements,like[[1.0][0.0],[0.1][0.9]]
        self.B = [[0.9, 0.1],
                  [0.2, 0.8]]

    def test_zeros(self):
        ''' Test the zeros function '''
        self.assertEqual(zeros(2,2), [[0,0], [0,0]])
        self.assertEqual(zeros(3,1), [[0],[0],[0]])
        self.assertEqual(zeros(3,2), [[0,0], [0,0],[0,0]])

    #def test_generate(self):
        '''Create a HMM and generate 100 observations'''
        #h = HMM(self.pi, self.A, self.B, self.V)
        #h.log.setLevel(logging.DEBUG)
        #for i in range(100):
            #h.gen()

    def test_forward(self):
        ''' fixme '''
        h = HMM(self.pi, self.A, self.B, self.V)
        h.log.setLevel(logging.DEBUG)
        h.calc_forward([0, 0])

    def test_backward(self):
        '''fixme '''
        h = HMM(self.pi, self.A, self.B, self.V)
        h.log.setLevel(logging.DEBUG)
        h.calc_backward([0, 0])

    def test_viterbi(self):
        '''fixme'''
        h = HMM(self.pi, self.A, self.B, self.V)
        h.log.setLevel(logging.DEBUG)
        h.viterbi([0, 0])
        #this is random set
        self.assertEqual(h.viterbi([0,0]), [0,0])
if __name__ == '__main__':
    unittest.main()

