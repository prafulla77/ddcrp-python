from pygraph.classes import digraph, graph
from pygraph.algorithms.cycles import find_cycle
from pygraph.algorithms.searching import breadth_first_search
from hyper_parameters import HyperParameters
from sampler_state import SamplerState
from sampler_state_tracker import SamplerStateTracker
from utils import  Util
from likelihood import DirichletLikeLihood
from data import Data
from scipy.sparse import csr_matrix as CRSMatrix
from math import log, exp

class GibbsSampler(object):
    def __init__(self):
        self.emptyTables =[]
        #A list of queues, each queue for maintaining a list of empty tables, which can be assigned when split
        # of tables happen.


    def doSampling(self, l):
        s = SamplerStateTracker.samplerStates[SamplerStateTracker.current_iter].copy()
        SamplerStateTracker.samplerStates.append(s)
        SamplerStateTracker.current_iter += 1
        all_observations = Data.getObservations()
        if len(self.emptyTables) != len(all_observations):
            for i in range(len(all_observations)):
                self.emptyTables.append([])
        for i in range(len(all_observations)):
            list = all_observations[i]
            for j in range(len(list)):
                self.sampleLink(j,i,l)

    def sampleLink(self, index, list_index, ll):
        s = SamplerStateTracker.samplerStates[SamplerStateTracker.current_iter]
        table_id = s.get_t(index, list_index)
        customersAtTable = s.getCustomersAtTable(table_id, list_index)
        orig_table_members = []
        g = digraph()
        ug = graph()
        for i in customersAtTable:
            orig_table_members.append(i)
            if not g.has_node(i):
                ug.add_node(i)
                g.add_node(i)
            j = s.getC(i, list_index)
            if not g.has_node(j):
                ug.add_node(j)
                g.add_node(j)
            g.add_edge((i,j))
            ug.add_edge((i,j))
        cycles = find_cycle(g)
        isCyclePresent = False
        if index in cycles:
            isCyclePresent = True
        if not isCyclePresent:
            # obs to sample moval will split the table into 2
            ug.del_edge((index, s.getC(index, list_index)))
            temp, new_table_members = breadth_first_search(ug, index)
            orig_table_members = new_table_members
            temp, old_table_members = breadth_first_search(ug, s.getC(index, list_index))
            s.setT(s.getT() + 1)
            s.setC(None, index, list_index)
            new_table_id = self.emptyTables[list_index].remove(0)
            for l in new_table_members:
                s.set_t(new_table_id, l , list_index)
            old_table_id = table_id
            s.setCustomersAtTable(set(old_table_members), old_table_id, list_index)
            table_id = new_table_id
            s.setCustomersAtTable(set(new_table_members), new_table_id, list_index)
        distanceMatrices = Data.getDistanceMatrices()
        distance_matrix = distanceMatrices[list_index]
        priors = distance_matrix[index]
        priors[index] = ll.getHyperParameters().getSelfLinkProb()
        sum_p = sum(priors)
        priors = priors/sum_p
        posterior = []
        indexes = []
        for i in range(len(priors)):
            if priors[i] != 0:
                indexes.append(i)
                table_proposed = s.get_t(i, list_index)
                if table_proposed == table_id:
                    posterior.append(priors[i])
                else:
                    proposedTableMembersSet = s.getCustomersAtTable(table_proposed, list_index)
                    proposed_table_members = list(proposedTableMembersSet)
                    change_in_log_likelihood = self.compute_change_in_likelihood(ll, orig_table_members,proposed_table_members, list_index)
                    posterior.append(exp(log(priors[i]+change_in_log_likelihood)))
        sample = Util.sample(posterior)
        customer_assignment_index = indexes[sample]
        assigned_table = s.get_t(customer_assignment_index, list_index)
        s.setC(customer_assignment_index, index, list_index)
        if assigned_table != table_id:
            s.setT(s.getT()-1)
            for members in orig_table_members:
                s.set_t(assigned_table, members, list_index)
            hs_orig_members_in_new_table = set(s.getCustomersAtTable(assigned_table, list_index))
            for i in range(len(orig_table_members)):
                hs_orig_members_in_new_table.add(orig_table_members[i])
            s.setCustomersAtTable(hs_orig_members_in_new_table, assigned_table, list_index)
            s.setCustomersAtTable(None, table_id, list_index)
            self.emptyTables[index].append(table_id)

    def compute_change_in_likelihood(self, l, orig_table_members, proposed_table_members, list_index):
        orig_table_loglikelihood = l.computeTableLogLikelihood(orig_table_members, list_index)
        proposed_table_loglikelihood = l.computeTableLogLikelihood(proposed_table_members, list_index)
        union_list = orig_table_members+proposed_table_members
        table_union_likelihood = l.computeTableLogLikelihood(union_list, list_index)
        return table_union_likelihood - orig_table_loglikelihood - proposed_table_loglikelihood