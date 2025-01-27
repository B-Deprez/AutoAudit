import pandas as pd
import pickle
import random

for i_seed in range(10):
    # Load the data and select the accounts as nodes
    edges = pd.read_csv('data/edge_data_synthetic.csv')

    # num nodes
    max_node = max(list(edges['source']) + list(edges['target']))+1
    print('Number of nodes:', max_node)

    # Get the list of nodes
    list_nodes = list(range(max_node))

    random.seed(i_seed)
    random.shuffle(list_nodes)
    map_id = {i: list_nodes[i] for i in range(max_node)}
    map_id_inv = {v: k for k, v in map_id.items()}

    # Map the nodes
    edges['source'] = edges['source'].map(map_id)
    edges['target'] = edges['target'].map(map_id)

    with open('data/synthetic_map_id_inv_'+str(i_seed)+'.pkl', 'wb') as f:
        pickle.dump(map_id_inv, f)

    # Save the edgelist
    edge_set = set(zip(edges['source'], edges['target']))
    with open('data/synthetic_edgelist_'+str(i_seed)+'.pkl', 'wb') as f:
        pickle.dump(edge_set, f)