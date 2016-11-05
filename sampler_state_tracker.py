from sampler_state import SamplerState
import random
random.seed()
class SamplerStateTracker(object):
    def __init__(self):
        self.current_iter = -1
        self.max_iter = 100
        self.samplerStates = []

    def returnCurrentSamplerState(self):
        if self.current_iter >= 0 and self.current_iter == len(self.samplerStates)-1 :
            return self.samplerStates[self.current_iter]
        else:
            return None

    def initializeSamplerState(self, list_observations):
        if self.current_iter == 0:
            num_data = 0
            for i in range(len(list_observations)):
                num_data += len(list_observations[i])
            state0 = SamplerState()
            state0.setNum_data(num_data)
            customer_assignments = []
            table_assignments = []
            topic_assignments_table = []
            topic_assignments_customer = []
            customersAtTableList = []
            count_each_topic = {}
            num_topics = 100
            for i in range(len(list_observations)):
                custome_assignment_per_list = []
                table_assignment_per_list = []
                topic_assignments_table_per_list = []
                topic_assignments_customer_per_list = []
                customersAtTable = {}
                for j in range(list_observations[i]):
                    custome_assignment_per_list.append(j)
                    table_assignment_per_list.append(j)
                    hs = set()
                    hs.add(j)
                    customersAtTable[j] = hs
                    topic = random.randint(0,num_topics)
                    topic_assignments_table_per_list.append(topic)
                    topic_assignments_customer_per_list.append(topic)
                    try:
                        count_each_topic[topic] += 1
                    except KeyError:
                        count_each_topic = 1
                customer_assignments.append(custome_assignment_per_list)
                table_assignments.append(table_assignment_per_list)
                customersAtTableList.append(customersAtTable)
                topic_assignments_table.append(topic_assignments_table_per_list)
                topic_assignments_customer.append(topic_assignments_customer_per_list)
            state0.setC(customer_assignments)
            state0.set_t(table_assignments)
            state0.setCustomerAtTableList(customersAtTableList)
            state0.setK_c(topic_assignments_customer)
            state0.setK_t(topic_assignments_table)
            state0.setT(num_data)
            state0.setK(num_topics)
            state0.setM(count_each_topic)
            self.current_iter = 0
            self.samplerStates.append(state0)

