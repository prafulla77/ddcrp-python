from scipy.sparse import csr_matrix as CRSMatrix
from copy import deepcopy
from sklearn.metrics import jaccard_similarity_score as jacc_sim

class SamplerState(object):
    def __init__(self):
        self.num_data = 0
        self.c = [] #[[]] c stores customer links
        self.t = [] #[[]] t stores table links
        self.T = 0 #number of occupied table at this iteration
        self.K = 0 #stores total number of topics
        self.k_c = [] #[[]] k_c stores topic assignments for each data point, topic assignment at the given table they are sitting
        self.k_t = [] #[[]] k_t stores topic assignment for each topic
        self.m = {} #stores number of tables assigned to each topic
        self.customersAtTableList = [] #keys are table_id, values are set of customer ids

        self.thetas = [] #list of CRSMatrix, multinomial parameter seen for each city, for each table in the city, understand it later

    def getNum_data(self):
        return self.num_data

    def setNum_data(self, num_data):
        self.num_data = num_data

    def getT(self):
        return self.T

    def setT(self, T):
        self.T = T

    def getK(self):
        return self.K

    def setK(self, K):
        self.K = K

    def getM(self):
        if __name__ == '__main__':
            return self.m

    def setM(self, m):
        self.m = m

    def getC(self, customer_index, city_index):
        if customer_index is None and city_index is None:
            return self.c
        else:
            return self.c[city_index][customer_index]

    def setC(self, c_or_customer_assignment, customer_index, city_index):
        if customer_index is None and city_index is None:
            self.c = c_or_customer_assignment
        else:
            self.c[city_index][customer_index] = c_or_customer_assignment

    def getK_c(self):
        return self.k_c

    def setK_c(self,k_c):
        self.k_c = k_c

    def getK_t(self):
        return self.k_t

    def setK_t(self, k_t):
        self.k_t =k_t

    def get_t(self, customer_index, city_index):
        if customer_index is None and city_index is None:
            return self.t
        else:
            return self.t[city_index][customer_index]

    def set_t(self, t_or_table_assignment, customer_index, city_index):
        if customer_index is None and city_index is None:
            self.t = t_or_table_assignment
        else:
            self.t[city_index][customer_index] = t_or_table_assignment

    def getCustomersAtTable(self, tableID, listIndex):
        try:
            return self.customersAtTableList[listIndex][tableID]
        except KeyError:
            return None

    def getCustomerAtTableList(self):
        return self.customersAtTableList

    def setCustomerAtTable(self, customers, tableID, listIndex):
        self.customersAtTableList[listIndex][tableID] = customers

    def setCustomerAtTableList(self, customerAtTableList):
        self.customersAtTableList = customerAtTableList

    def __copy__(self):
        #verify this later what all to be copied
        newone = SamplerState()
        newone.c = deepcopy(self.c)
        newone.t = deepcopy(self.t)
        newone.customersAtTableList = deepcopy(self.customersAtTableList)
        return newone

    def prettyPrint(self):
        print "Total number of observations are ==> ", self.num_data
        print "Total number of documents are ==> ", len(self.c)
        print "Total number of tables are ==> ", self.T
        print "Total number of topics are ==> ", self.K

    def getTableSeatingsSet(self): #returns set of sets of customer siting at each table, for each city
        tableSeatings = []
        for cityTables in self.t:
            tableMembers = {}
            cityTableSeatings = set()
            for i in range(len(cityTables)):
                tab = cityTables[i]
                try:
                    tableTabMembers = tableMembers[tab]
                except KeyError:
                    tableMembers[tab] = set()
                    tableTabMembers = tableMembers[tab]
                tableTabMembers.add(i)
                tableMembers[tab] = tableTabMembers
            for value in tableMembers.values():
                cityTableSeatings.add(value)
            tableSeatings.append(cityTableSeatings)
        return tableSeatings

    def tableJaccardSimilarity(self, SamplerState):
        seatingsA = self.getTableSeatingsSet()
        seatingsB = SamplerState.getTableSeatingsSet()
        similarity = 0.0
        for i in range(len(seatingsA)):
            similarity += jacc_sim(seatingsA[i], seatingsB[i], normalize=True)
        return similarity

    def __eq__(self, other):
        if isinstance(other, SamplerState):
            return self.getTableSeatingsSet() == other.getTableSeatingsSet()

    #hash code function missing, check if required