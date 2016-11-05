from hyper_parameters import HyperParameters
from data import Data
import math

class DirichletLikeLihood(object):
    def __init__(self, HyperParameters = None):
        self.HyperParameters = HyperParameters
        self.cachedGammaValues = {}

    def ComputeTableLogLikelihood(self, table_members, list_index): #table_members = [], list_index = 0
        list_observations = Data.getObservations() #resolve this later
        observations = list_observations[list_index]
        obs_category_count = {} #store index of venue category and respective counts of table members, resolve this later
        for i in range(len(table_members)):
            obs_category = observations[table_members[i]]
            try:
                obs_category_count[obs_category] += 1
            except KeyError:
                obs_category_count = 1
        dirichletParams = self.HyperParameters.getDirichletParam()
        sum_venue_cat_alpha = 0.0
        sum_log_gamma_sum_venue_cat_alpha = 0.0
        sum_alpha = 0.0
        sum_log_gamma_alpha = 0.0
        for i in range(len(dirichletParams)):
            try:
                category_count = obs_category_count[i]
            except KeyError:
                category_count = 0
            sum_alpha += dirichletParams[i]
            sum_venue_cat_alpha += dirichletParams[i] + category_count
            sum_log_gamma_sum_venue_cat_alpha += self.logGamma(dirichletParams[i]+category_count)
            sum_log_gamma_alpha += self.logGamma(dirichletParams[i])
        log_numerator = sum_log_gamma_sum_venue_cat_alpha - self.logGamma(sum_venue_cat_alpha)
        log_denominator = sum_log_gamma_alpha - math.lgamma(sum_alpha)
        log_likelihood = log_numerator - log_denominator
        return  log_likelihood

    def logGamma(self, index):
        try:
            return self.cachedGammaValues[index]
        except KeyError:
            log_gamma = math.lgamma(index)
            self.cachedGammaValues[index] = log_gamma
            return  log_gamma

    #port this, if required
    '''
    public double computeFullLogLikelihood(ArrayList<HashMap<Integer, HashSet<Integer>>> customersAtTableList) {
		double ll = 0;
		for (int listIndex=0; listIndex<customersAtTableList.size(); listIndex++) {
			HashMap<Integer, HashSet<Integer>> customersAtTable = customersAtTableList.get(listIndex);
			for (Integer tableId : customersAtTable.keySet()) {
				if (customersAtTable.get(tableId) != null) {
					HashSet<Integer> hs = customersAtTable.get(tableId);
					ArrayList<Integer> tableMembers = new ArrayList<Integer>(hs);
					ll += computeTableLogLikelihood(tableMembers, listIndex);
				}
			}
		}
		return ll;
	}
    '''