from sampler_state_tracker import SamplerStateTracker
class Posterior(object):
    def __init__(self):
        self.counts = [] #number of observations of each state
        self.probabilities = [] #estimated probability of each observed state in the estimated joint distribution
        self.states = [] #possible sampler states
        self.burnInPeriod = 0 #number of samples to ignore
        self.numSamples= 0 #number of Gibbs samples computed
        self.normConst = 0 #normalizing constant (numSamples-burnInPeriod)

    def estimatePosterior(self, burnInPeriod):
        self.burnInPeriod = burnInPeriod
        states = SamplerStateTracker.samplerStates
        self.numSamples = len(states)
        countsMap = {} #SamplersState -> integer
        for i in range(self.burnInPeriod+1, self.numSamples):
            s = states[i]
            try:
                countsMap[s] += 1
            except KeyError:
                countsMap[s] = 1
        n = 0
        for s in countsMap:
            c = countsMap[s]
            n += c
            self.counts.append(c)
            self.states.append(s)
        self.normConst = n
        if n>0:
            self.probabilities.append(c/float(n))

    def prettyPrint(self):
        print "Total number of states are ==> ", len(self.probabilities)
        print "Probabilities: "
        probs = ''
        for p in self.probabilities:
            probs += str(p)+', '
        print probs
