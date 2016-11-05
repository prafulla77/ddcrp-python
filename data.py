class Data(object):
    def __init__(self):
        self.list_observations = [] #list of list of event features
        self.distanceMatrices = [] #list of sparse matrix for storing distance (* not clear now, see later)

    def populateObservationList(self):
        pass

    def populateDistanceMatrices(self):
        pass

    def getObservations(self):
        if len(self.list_observations) == 0:
            self.populateObservationList()
        return self.list_observations

    def getDistanceMatrices(self):
        if len(self.distanceMatrices == 0):
            self.populateDistanceMatrices()
        return  self.distanceMatrices
