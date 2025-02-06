import pandas as pd
import pickle
import random

def generate_synthetic_permutations(string_name):
    for i_seed in range(10):
        # Load the data and select the accounts as nodes
        edges = pd.read_csv('data/edge_data_'+string_name+'.csv')

        # num nodes
        max_node = max(list(edges['source']) + list(edges['target']))+1

        # Get the list of nodes
        list_nodes = list(range(max_node))

        random.seed(i_seed)
        random.shuffle(list_nodes)
        map_id = {i: list_nodes[i] for i in range(max_node)}
        map_id_inv = {v: k for k, v in map_id.items()}

        # Map the nodes
        edges['source'] = edges['source'].map(map_id)
        edges['target'] = edges['target'].map(map_id)

        with open('data/map_id_inv_'+string_name+str(i_seed)+'.pkl', 'wb') as f:
            pickle.dump(map_id_inv, f)

        # Save the edgelist
        edge_set = set(zip(edges['source'], edges['target']))
        with open('data/edgelist_'+string_name+str(i_seed)+'.pkl', 'wb') as f:
            pickle.dump(edge_set, f)

n_nodes_list = [100, 10000, 100000] # Number of nodes in the graph
m_edges_list = [1, 2, 5] # Number of edges to attach from a new node to existing nodes
p_edges_list = [0.001, 0.01] # Probability of adding an edge between two nodes
generation_method_list = [
    'Barabasi-Albert', 
    'Erdos-Renyi', 
    'Watts-Strogatz'
    ] # Generation method for the graph
n_patterns_list = [3, 5] # Number of smurfing patterns to add


results_all = dict()

for n_nodes in n_nodes_list:
    for n_patterns in n_patterns_list:
        if n_patterns <= 0.06*n_nodes:
            for generation_method in generation_method_list:
                if generation_method == 'Barabasi-Albert':
                    p_edges = 0
                    for m_edges in m_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        generate_synthetic_permutations(string_name)
                if generation_method == 'Erdos-Renyi':
                    m_edges = 0
                    for p_edges in p_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        generate_synthetic_permutations(string_name)

                if generation_method == 'Watts-Strogatz':
                    for m_edges in m_edges_list:
                        for p_edges in p_edges_list:
                            string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                            generate_synthetic_permutations(string_name)