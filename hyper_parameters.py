class HyperParameters(object):
    def __init__(self, VOCAB_SIZE = 0, dirichletParam = [], selfLinkProb = 0.0):
        self.VOCAB_SIZE = VOCAB_SIZE
        self.dirichletParam = dirichletParam
        self.selfLinkProb = selfLinkProb

    def getVocabSize(self):
        return self.VOCAB_SIZE

    def getDirichletParam(self):
        return self.dirichletParam

    def getSelfLinkProb(self):
        return self.selfLinkProb
