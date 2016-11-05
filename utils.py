from sampler_state import SamplerState
from sampler_state_tracker import SamplerStateTracker
import random

class Util(object):

    def sample(self, probs):
        cumulative_probs = []
        sum_probs = 0.0
        for prob in probs:
            sum_probs += prob
            cumulative_probs.append(prob)
        if sum_probs != 1.0:
            for i in range(len(probs)):
                probs[i] /= sum_probs
                cumulative_probs[i] /= sum_probs
        random_thres = random.random()
        for i in range(len(cumulative_probs)):
            if cumulative_probs[i] > random_thres:
                return i
        return -1

    def printTableConfiguration(self, list_index):
        pass
        # do it later

    def testSamplerStateEquals(self):
        pass
        # do it later