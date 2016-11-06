from random import randint
class hdp_state(object):
    def __init__(self):
        self.num_data = 0
        self.cust_links = []
        self.table_links = []
        self.num_occupied_tables = 0
        self.num_clusters = 0
        self.cluster_assignment_cust = [] # cluster assignments for each data customer
        self.cluster_assignment_table = [] #[[]] cluster assignments for each table
        self.num_tables_per_cluster = {} #stores number of tables assigned to each cluster
        self.customers_at_table_list = [] # list of dictionaries, dictionary: keys are table_id, values are set of customer ids

class hdp_state_tracker(object):
    def __init__(self, max_iter=500):
        self.cur_iter = -1
        self.max_iter = max_iter
        self.hdp_states = []

    def return_current_sampler_state(self):
        if self.cur_iter >= 0 and self.cur_iter == len(self.sampler_states)-1 :
            return self.sampler_states[self.cur_iter]
        else:
            return None

    def initialize_sampler_state(self, list_observations):
        if self.cur_iter == -1:
            num_data = 0
            for l_o in list_observations:
                num_data += len(l_o)
            hdp_state_0 = hdp_state()
            hdp_state_0.num_data = num_data
            customer_links= []
            table_links = []
            cluster_assignment_customer = []
            cluster_assignment_table = []
            customers_at_table_list = []
            num_tables_per_cluster = {}
            num_clust = 100 # Random number
            for l_o in list_observations:
                customer_links_per_list = []
                table_links_per_list = []
                cluster_assignment_customer_per_list = []
                cluster_assignment_table_per_list = []
                customers_at_table = {}
                for j in range(len(l_o)):
                    customer_links_per_list.append(j)
                    table_links_per_list.append(j)
                    hs = set(j)
                    customers_at_table[j] = hs
                    cluster = randint(0,num_clust)
                    cluster_assignment_customer_per_list.append(cluster)
                    cluster_assignment_table_per_list.append(cluster)
                    try:
                        num_tables_per_cluster[cluster] += 1
                    except KeyError:
                        num_tables_per_cluster[cluster] = 1
                customer_links.append(customer_links_per_list)
                table_links.append(table_links_per_list)
                customers_at_table_list.append(customers_at_table)
                cluster_assignment_customer.append(cluster_assignment_customer_per_list)
                cluster_assignment_table.append(cluster_assignment_table_per_list)
            hdp_state_0.cust_links = customer_links
            hdp_state_0.table_links = table_links
            hdp_state_0.customers_at_table_list = customers_at_table_list
            hdp_state_0.cluster_assignment_cust = cluster_assignment_customer
            hdp_state_0.cluster_assignment_table = cluster_assignment_table
            hdp_state_0.num_data = num_data
            hdp_state_0.num_clusters = num_clust
            hdp_state_0.num_tables_per_cluster = num_tables_per_cluster
            self.hdp_states.append(hdp_state_0)
            self.cur_iter = 0

class hyper_parameter(object):
    def __init__(self, vocab_size, num_docs, dirichlet_param, self_link_prob_cust, self_link_prob_table):
        self.vocab_size = vocab_size
        self.num_docs = num_docs
        self.dirichlet_param = dirichlet_param
        self.self_link_prob_cust = self_link_prob_cust
        self.self_link_prob_table = self_link_prob_table
