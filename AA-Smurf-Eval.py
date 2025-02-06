import pickle
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score
import numpy as np


def evaluate_AA_Smurf(string_name):
    columns = ['laundering', 'separate', 'new_mules', 'existing_mules']
    AUC_ROC_dict = dict()
    AUC_PR_dict = dict()
    for column in columns:
        AUC_ROC_dict[column] = []
        AUC_PR_dict[column] = []

    for i_seed in range(5):
        with open('results/order_'+string_name+str(i_seed)+'.pkl', 'rb') as handle:
            order_nodes = pickle.load(handle)
        with open('data/map_id_inv_'+string_name+str(i_seed)+'.pkl', 'rb') as handle:
            map_id_inv = pickle.load(handle)
        order_nodes_og = [map_id_inv[i] for i in order_nodes]

        map_scores = dict()
        for j in range(len(order_nodes_og)):
            node = order_nodes_og[j]
            score = (len(order_nodes_og)-j)/len(order_nodes_og)
            map_scores[node] = score

        # Load the label data
        label_data = pd.read_csv('data/label_data_'+string_name+'.csv')
        label_data['node'] = label_data.index
        label_data['score'] = label_data['node'].map(map_scores)
        label_data['score'] = label_data['score'].fillna(0)

        # Calculate the AUC-ROC and AUC-PR
        for column in columns:
            AUC_ROC = roc_auc_score(label_data[column], label_data['score'])
            AUC_PR = average_precision_score(label_data[column], label_data['score'])
            AUC_ROC_dict[column].append(AUC_ROC)
            AUC_PR_dict[column].append(AUC_PR)

    results = dict()
    for column in columns:
        AUC_ROC_list = AUC_ROC_dict[column]
        AUC_PR_list = AUC_PR_dict[column]
        results[column] = (np.mean(AUC_ROC_list), np.mean(AUC_PR_list))
    return results

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
                        print("======"+string_name+"======")
                        result_int = evaluate_AA_Smurf(string_name)
                        results_all[string_name] = result_int
                if generation_method == 'Erdos-Renyi':
                    m_edges = 0
                    for p_edges in p_edges_list:
                        string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                        print("======"+string_name+"======")
                        result_int = evaluate_AA_Smurf(string_name)
                        results_all[string_name] = result_int
                if generation_method == 'Watts-Strogatz':
                    for m_edges in m_edges_list:
                        for p_edges in p_edges_list:
                            string_name = 'synthetic_' + generation_method + '_'  + str(n_nodes) + '_' + str(m_edges) + '_' + str(p_edges) + '_' + str(n_patterns)
                            print("======"+string_name+"======")
                            result_int = evaluate_AA_Smurf(string_name)
                            results_all[string_name] = result_int

results_df = pd.DataFrame(results_all)
results_df.to_csv("synthetic_autoaudit_combined.csv")