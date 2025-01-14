import pandas as pd
import pickle

data_set = 'HI-Small'
# Load the data and select the accounts as nodes
transactions_df = pd.read_csv('data/'+data_set+'_Trans.csv')
edges = transactions_df[['Account', 'Account.1']] # Get the edges
node_list = list(set(edges['Account']).union(set(edges['Account.1']))) # Get the unique accounts

# Create mapping from accounts to integers (for the adjacency matrix)
map_id = {node: idx for idx, node in enumerate(node_list)}
# Save the inverse mapping to link scores back to accounts
map_id_inv = {idx: node for idx, node in enumerate(node_list)}
with open('data/'+data_set+'_map_id_inv.pkl', 'wb') as f:
    pickle.dump(map_id_inv, f)

# Map the accounts to integers
edges['Account'] = edges['Account'].map(map_id)
edges['Account.1'] = edges['Account.1'].map(map_id)

# Save the edgelist
edge_set = set(zip(edges['Account'], edges['Account.1']))
with open('data/'+data_set+'_edgelist.pkl', 'wb') as f:
    pickle.dump(edge_set, f)