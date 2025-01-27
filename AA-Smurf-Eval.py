import pickle
import pandas as pd
from sklearn.metrics import roc_auc_score, average_precision_score
import numpy as np

AUC_ROC_list = []
AUC_PR_list = []

for i_seed in range(10):
    with open('results/synthetic_order_'+str(i_seed)+'.pkl', 'rb') as handle:
        order_nodes = pickle.load(handle)
    with open('data/synthetic_map_id_inv_'+str(i_seed)+'.pkl', 'rb') as handle:
        map_id_inv = pickle.load(handle)
    order_nodes_og = [map_id_inv[i] for i in order_nodes]

    map_scores = dict()
    for j in range(len(order_nodes_og)):
        node = order_nodes_og[j]
        score = (len(order_nodes_og)-j)/len(order_nodes_og)
        map_scores[node] = score

    # Load the label data
    label_data = pd.read_csv('data/label_data_synthetic.csv')
    label_data['node'] = label_data.index
    label_data['score'] = label_data['node'].map(map_scores)

    # Calculate the AUC-ROC and AUC-PR
    AUC_ROC = roc_auc_score(label_data['laundering'], label_data['score'])
    AUC_PR = average_precision_score(label_data['laundering'], label_data['score'])

    AUC_ROC_list.append(AUC_ROC)
    AUC_PR_list.append(AUC_PR)
print('AUC-ROC:', np.mean(AUC_ROC_list))
print('AUC-PR:', np.mean(AUC_PR_list))
