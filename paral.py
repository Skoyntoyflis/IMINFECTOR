#Importing necessary libraries
import math
import numpy as np # linear algebra, not needed
import pandas as pd #for data processing/handling csv file 
from matplotlib import pyplot as plt #for ploting charts
import seaborn as sns #visualization/for ploting heatmap
import igraph as ig
# import rdkit
import networkx as nx
import multiprocessing as mp
import timebudget 


# timebudget.set_quiet()  # don't show measurements as they happen
# timebudget.report_at_exit()  # Generate report when the program exits

# #Start
# g = ig.Graph.Read_Ncol("Digg_network.txt")
# G = g.to_networkx()
# H = G.to_undirected()
# len=H.number_of_nodes()


# print("start")
# preds = nx.jaccard_coefficient(H)
# print("end")
# print(preds)
# to_add=[]
# count = 0 
# count2=0

# def complex_operation(input_index):
#    print("Complex operation. Input index: {:2d}".format(input_index))
#    [to_add.append([u,v,p]) for u,v,p in preds]
#    #[math.exp(i) * math.sinh(i) for i in [1] * iterations_count]


# @timebudget
# def run_complex_operations(operation, input, pool):
#     pool.map(operation, input)

# processes_count = 10


# if __name__ == '__main__':
#     processes_pool = Pool(processes_count)
#     run_complex_operations(complex_operation, (preds_split, range(20)), processes_pool) 

g = ig.Graph.Read_Ncol("Data/Digg/Digg_network.txt")

G = g.to_networkx()
H = G.to_undirected()


def my_jaccard_coefficient(G, u, v):
    
    cnbors = list(nx.common_neighbors(G, u, v))
    union_size = len(set(G[u]) | set(G[v]))
    if union_size == 0:
        return 0
    else:
        return len(cnbors) / union_size


to_add=[]
length =H.number_of_nodes()
visited=[]
count = 0 
count2 = 0
for u in H.nodes:
    count2+=1
    for v in H.nodes:
        if v not in visited:
           p = my_jaccard_coefficient(H,u,v)
           if p>=0.9:        
            to_add.append([u,v,p])
            count +=1
            print("At",count2, "total = ", count, "with p = ", p)
    visited.append(u)